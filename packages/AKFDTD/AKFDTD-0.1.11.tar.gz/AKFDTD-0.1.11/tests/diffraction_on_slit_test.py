# pip install AKFDTD
from FDTD.fdtd2D import EM2D
# or
# from AKFDTD.FDTD.fdtd2D import EM2D

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Parameters
from matplotlib.widgets import Slider


if __name__ == "__main__":
    # display PML region
    show_PML = False

    # display of the field distribution along the center of the calculation area
    show_xy = False
    # show_xy = True

    # incoming plane wave wavelength
    wavelength_init = 3
    # slit width
    slit_width_init = 3

    # create FDTD domain and initialize fields
    fields = EM2D(Lx=20., Ly=20., Nx=200, Ny=201, wavelength=wavelength_init)
    fields.add_slit(slit_width_init)

    # # Initial condition: sinusoidal wave
    # if True:
    if False:
        # Initial condition: sinusoidal wave
        N_cycles = 1
        x_init = -0.5
        fields.init_fields()
        fields.init_wave(x_init)
    else:
        N_cycles = 500
        fields.start(N_cycles)

    # create a matplotlib window to display the 2D field distribution, the output field intensity, and two sliders (for wavelength and for slit width)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6))

    x = fields.get_x(show_PML)
    y = fields.get_y(show_PML)
    im1 = ax1.imshow(fields.get_Ez(show_PML), extent=(x.min(), x.max(), y.max(), y.min()),
                     cmap='RdBu', origin='upper', vmin=-2, vmax=2)
    # cax = fig.colorbar(im1, ax=ax1)
    # Add a title and labels
    ax1.set_xlabel('y-axis')
    ax1.set_ylabel('y-axis')

    if show_xy:
        im2, = ax2.plot(fields.x, abs(fields.Ez[:, fields.Ny // 2 + 0 * (fields.pml_width + 2)]))
    else:
        im2, = ax2.plot(y, fields.get_out_intensity(show_PML))
        ax2.set_xlim(y.min(), y.max())
    # ax2.set_ylim(0, 1.6)
    ax2.set_xlabel('y-axis')
    ax2.set_ylabel('intensity')

    ax1.set_position([0.1, 0.55, 0.8, 0.4])  # [left, bottom, width, height]
    out = ax1.get_position()
    ax2.set_position([out.x0, 0.25, out.x1 - out.x0, 0.2])

    # Create a slider axis and slider widget
    slider_ax1 = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor='lightgoldenrodyellow')
    slider_ax2 = plt.axes([0.2, 0.05, 0.6, 0.05], facecolor='lightgoldenrodyellow')
    wavelength_slider = Slider(slider_ax1, 'wavelength', 1., 5.0, valinit=wavelength_init)
    slitwidth_slider = Slider(slider_ax2, 'slit width', 1., 6., valinit=slit_width_init)

    # Time-stepping loop
    def update(n):
        fields.update()

        if fields.n_step % 10 == 0:
            # Update the image data
            im1.set_data(fields.get_Ez(show_PML))
            if show_xy:
                im2.set_ydata(abs(fields.Ez[:, fields.Ny // 2 + 0 * (fields.pml_width + 2)]))
            else:
                im2.set_ydata(fields.get_out_intensity(show_PML))
            ax2.relim()  # Recalculate limits based on new data
            ax2.autoscale_view()  # Rescale the view

        # return [im1, im2]

    # Update functions for slider
    def slider_update_wavelength(val):
        fields.set_wavelength(wavelength=val)
        fields.start(N_cycles)

    def slider_update_slit_width(val):
        fields.add_slit(slit_width=val)
        fields.start(N_cycles)

    # Connect the slider to the update function
    wavelength_slider.on_changed(slider_update_wavelength)
    slitwidth_slider.on_changed(slider_update_slit_width)

    # Animation setup
    ani = FuncAnimation(fig, update, frames=100, interval=10)

    # display matplotlib plot
    plt.show()
