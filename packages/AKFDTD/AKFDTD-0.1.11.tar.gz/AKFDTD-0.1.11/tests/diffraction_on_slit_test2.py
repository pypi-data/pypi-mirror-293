from FDTD.fdtd2D import EM2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors


# Create a colormap from red to blue
cmap = plt.colormaps.get_cmap('Spectral_r')


def wavelength_to_color(wavelength, norm):
    # Normalize the wavelength
    norm_wavelength = norm(wavelength)
    # Get the color from the colormap
    color = cmap(norm_wavelength)[:-1]
    colors = [(0, 0, 0), color, (1, 1, 1)]  # Black -> Color
    n_bins = 100  # Number of bins for interpolation
    cmap_name = 'black_color'
    return LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)


if __name__ == "__main__":
    # display PML region
    show_PML = False

    # display absolute value of the Poynting vector
    show_Poynting = True

    # display of the field distribution along the center of the calculation area
    show_xy = False
    # show_xy = True

    # incoming plane wave wavelength
    wavelength_init = 3.
    wavelength_min = 1.
    wavelength_max = 5.
    # Normalize the wavelength to be between 0 and 1 for colormap
    norm = mcolors.Normalize(vmin=wavelength_min, vmax=wavelength_max)

    # simulation domain
    Lx = 30
    Ly = 20
    Nx = 300
    Ny = 201

    # slit width
    slit_width_init = 3
    slit_position_init = -Lx/2 + 8

    # create FDTD domain and initialize fields
    fields = EM2D(Lx=Lx, Ly=Ly, Nx=Nx, Ny=Ny, wavelength=wavelength_init)
    fields.add_slit(width=slit_width_init, position=slit_position_init)

    # Initial condition
    N_cycles = 500

    # create a matplotlib window to display the 2D field distribution, the output field intensity,
    # and two sliders (for wavelength and for slit width)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 7))

    x = fields.get_x(show_PML)
    y = fields.get_y(show_PML)
    if show_Poynting:
        cm = wavelength_to_color(wavelength_init, norm)
        out_field = fields.start_until(None)
        im1 = ax1.imshow(out_field, extent=(y.min(), y.max(), x.max(), x.min()),
                         cmap=cm, origin='upper')
    else:
        fields.start_until(N_cycles)
        out_field = fields.get_Ez(show_PML)
        # out_field = fields.get_Sx(show_PML)
        im1 = ax1.imshow(out_field, extent=(y.min(), y.max(), x.max(), x.min()),
                         cmap='RdBu', origin='upper', vmin=-2, vmax=2)
    # cax = fig.colorbar(im1, ax=ax1)
    # Add a title and labels
    ax1.set_xlabel('y-axis')
    ax1.set_ylabel('x-axis')

    if show_xy:
        im2, = ax2.plot(fields.x, abs(fields.Ez[:, fields.Ny // 2 + 0 * (fields.pml_width + 2)]))
    else:
        im2, = ax2.plot(y, fields.get_out_intensity(show_PML))
        ax2.set_xlim(y.min(), y.max())
    # ax2.set_ylim(0, 1.6)
    ax2.set_xlabel('y-axis')
    ax2.set_ylabel('intensity')

    ax1.set_position([0.1, 0.5, 0.8, 0.45])  # [left, bottom, width, height]
    out = ax1.get_position()
    ax2.set_position([out.x0, 0.27, out.x1 - out.x0, 0.15])

    # Create a slider axis and slider widget
    slider_ax1 = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor='lightgoldenrodyellow')
    slider_ax2 = plt.axes([0.2, 0.05, 0.6, 0.05], facecolor='lightgoldenrodyellow')
    wavelength_slider = Slider(slider_ax1, 'wavelength', wavelength_min, wavelength_max, valinit=wavelength_init)
    slitwidth_slider = Slider(slider_ax2, 'slit width', 1., 10., valinit=slit_width_init)
    # Create a CheckButtons widget
    poynting_ax = plt.axes([0.03, 0.15, 0.4, 0.04])  # Position for the checkbox
    poynting_check = CheckButtons(poynting_ax, ['display energy flow'], [show_Poynting])

    def update_ax1():
        if show_Poynting:
            global out_field
            im1.set_data(out_field)
            im1.autoscale()  # Autoscale to update color limits if needed
        else:
            out_field = fields.get_Ez(show_PML)
            # out_field = fields.get_Sx(show_PML)
            im1.set_data(out_field)

    def update_ax2():
        if show_xy:
            im2.set_ydata(abs(fields.Ez[:, fields.Ny // 2 + 0 * (fields.pml_width + 2)]))
        else:
            im2.set_ydata(fields.get_out_intensity(show_PML))

        ax2.relim()  # Recalculate limits based on new data
        ax2.autoscale_view()  # Rescale the view

    # Time-stepping loop
    def update(n):
        fields.update()
        if show_Poynting:
            global out_field
            fields.accumulator += fields.get_S()
            if fields.n_step % fields.Nt == 0:
                dS = fields.norm(out_field)
                print(f"S = {dS}")
                if dS < 0.5:
                    ani.event_source.stop()  # Pause the animation
                else:
                    out_field = fields.accumulator
                    update_ax1()
                    fields.accumulator = 0
            update_ax2()
        else:
            update_ax1()
            if fields.n_step % fields.Nt == 0:
                update_ax2()

    def start_update():
        if show_Poynting:
            # Update the fields until saturation
            global out_field
            fields.accumulator = 0
            out_field = fields.start_until(None)
        else:
            fields.start_until(N_cycles)
        update_ax1()

    # Update functions for sliders
    def slider_update_wavelength(val):
        ani.event_source.stop()  # Pause the animation

        if show_Poynting:
            # Update the colormap
            im1.set_cmap(wavelength_to_color(val, norm))
        # Update the wavelength
        fields.set_wavelength(wavelength=val)
        # Update the fields
        start_update()

        ani.event_source.start()  # Resume the animation

    def slider_update_slit_width(val):
        ani.event_source.stop()  # Pause the animation

        # change slit
        fields.add_slit(width=val, position=slit_position_init)
        # Update the fields
        start_update()

        ani.event_source.start()  # Resume the animation

    # Define the function to toggle the visibility of the plot lines
    def toggle_poynting(label):
        global show_Poynting
        ani.event_source.stop()  # Pause the animation

        status = poynting_check.get_status()  # Get the status of the checkboxes
        if status[0]:
            show_Poynting = True
            global out_field
            new_cmap = wavelength_to_color(fields.wavelength, norm)
            im1.set_cmap(new_cmap)  # Update the colormap
            out_field = fields.do_n(fields.Nt, accumulate=True)
            update_ax1()
        else:
            show_Poynting = False
            im1.set_cmap('RdBu')  # Update the colormap
            im1.set_clim(-2, 2)

        ani.event_source.start()  # Resume the animation

    # Connect the slider to the update function
    wavelength_slider.on_changed(slider_update_wavelength)
    slitwidth_slider.on_changed(slider_update_slit_width)
    # Connect the CheckButtons widget with the toggle function
    poynting_check.on_clicked(toggle_poynting)

    # Animation setup
    ani = FuncAnimation(fig, update, frames=100, interval=10)

    # display matplotlib plot
    plt.show()
