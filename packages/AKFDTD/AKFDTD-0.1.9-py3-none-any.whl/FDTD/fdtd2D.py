import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
from timeit import default_timer as timer


# Parameters
from matplotlib.widgets import Slider


is_DEBUG = False
# is_DEBUG = True


# Damping profiles
def damping_profile(x, width, max_value, p_pml):
    """
    Damping profile.
    """
    return max_value * (x / width)**p_pml


def d_dx(u, dx):
    return np.diff(u, axis=0) / dx


def d_dy(u, dy):
    return np.diff(u, axis=1) / dy


class EM2D:
    def __init__(self, Lx=20., Ly=20., Nx=200, Ny=201, wavelength=3, exponential_PML=True):
        self.exponential_PML = exponential_PML
        if self.exponential_PML:
            self.update = self.update_2
        else:
            self.update = self.update_1
        self.apply_PEC = lambda: None

        # field components
        self.Ezx = None
        self.Ezy = None
        self.Ez = None
        self.Hx = None
        self.Hy = None
        self.I_out = None

        # Wave velocity
        self.c = 1

        # Wavelength
        self.wavelength = None
        self.k = None
        self.omega = None
        self.set_wavelength(wavelength)

        # time step
        self.n_step = 0

        self.Lx = Lx
        self.Ly = Ly
        self.Nx = None
        self.Ny = None
        self.dx = None
        self.dy = None
        self.dt = None
        self.init_domain(Lx, Ly, Nx, Ny)

        self.x = None
        self.y = None
        self.create_grid()

        self.pml_width = None
        self.sigma_max = None
        self.pml_p = None
        self.set_PML()

        self.exp_sy_Ezx = None
        self.exp_sx_Ezy = None
        self.exp_sy_Hx = None
        self.exp_sx_Hy = None
        self.sy_Ezx = None
        self.sx_Ezy = None
        self.sy_Hx = None
        self.sx_Hy = None
        self.init_PML()

        # self.init_fields()
        self.out_pos = -self.pml_width - 2

    def set_wavelength(self, wavelength):
        # Wavelength of the incident wave
        self.wavelength = wavelength
        # λ = c / f -> f = c / λ
        # Wave number
        self.k = 2 * np.pi / self.wavelength
        # Angular frequency
        self.omega = self.c * self.k

    def init_domain(self, Lx, Ly, Nx, Ny):
        """
        Init domain
        """
        # domain size
        self.Lx = Lx
        self.Ly = Ly

        # number of grid points
        self.Nx = Nx
        self.Ny = Ny

        self.dx = self.Lx / self.Nx  # grid spacing in x direction
        self.dy = self.Ly / self.Ny  # grid spacing in y direction

        self.dt = 0.75 / np.sqrt(1 / self.dx ** 2 + 1 / self.dy ** 2)  # time step size (stability criterion)

    def set_PML(self, pml_width=20, pml_p=2):
        """
        Init PML parameters
        """
        # PML parameters
        self.pml_width = pml_width

        # maximum sigma value for PML
        self.sigma_max = 1 / self.dt

        # order of sigma function
        self.pml_p = pml_p
        # self.pml_p = 3

    def init_PML(self):
        # PML damping profiles
        sigma_x = np.zeros(self.Nx)
        sigma_y = np.zeros(self.Ny)
        sigma_Hx = np.zeros(self.Nx - 1)
        sigma_Hy = np.zeros(self.Ny - 1)

        i_pml = np.arange(1, self.pml_width+1)
        sigma_x[range(self.pml_width-1, -1, -1)]\
            = sigma_y[range(self.pml_width-1, -1, -1)]\
            = sigma_x[-self.pml_width:]\
            = sigma_y[-self.pml_width:]\
            = damping_profile(i_pml, self.pml_width, self.sigma_max, self.pml_p)

        sigma_Hx[range(self.pml_width-1, -1, -1)]\
            = sigma_Hy[range(self.pml_width-1, -1, -1)]\
            = sigma_Hx[-self.pml_width:]\
            = sigma_Hy[-self.pml_width:]\
            = damping_profile(i_pml - 0.5, self.pml_width, self.sigma_max, self.pml_p)

        C = self.dt / 2
        sy_Ezx = sigma_y[np.newaxis, 1:-1] * C
        sx_Ezy = sigma_x[1:-1, np.newaxis] * C
        sy_Hx = sigma_Hy[np.newaxis, :] * C
        sx_Hy = sigma_Hx[:, np.newaxis] * C

        if self.exponential_PML:
            self.exp_sy_Ezx = np.exp(-sy_Ezx)
            self.exp_sx_Ezy = np.exp(-sx_Ezy)
            self.exp_sy_Hx = np.exp(-sy_Hx)
            self.exp_sx_Hy = np.exp(-sx_Hy)
        else:
            self.sy_Ezx = sy_Ezx
            self.sx_Ezy = sx_Ezy
            self.sy_Hx = sy_Hx
            self.sx_Hy = sx_Hy

    def init_fields(self):
        """
        Init fields
        """
        # z-component of the electric field (1)
        self.Ezx = np.zeros((self.Nx, self.Ny))
        # z-component of the electric field (2)
        self.Ezy = np.zeros((self.Nx, self.Ny))
        self.Ez = self.Ezx + self.Ezy

        # x-component of the magnetic field
        self.Hx = np.zeros((self.Nx-2, self.Ny-1))
        # y-component of the magnetic field
        self.Hy = np.zeros((self.Nx-1, self.Ny-2))

        self.I_out = 0

    def create_grid(self):
        """
        Create grid
        """
        self.x = np.linspace(-self.Lx/2, self.Lx/2, self.Nx)
        self.y = np.linspace(-self.Ly/2, self.Ly/2, self.Ny)
        # X, Y = np.meshgrid(x, y, indexing="ij")

    def update_2(self):
        self.n_step += 1
        if is_DEBUG:
            start = timer()

        C = self.dt/self.c
        # Update Ez (electric field component)
        self.Ezx[1:-1, 1:-1] = self.exp_sy_Ezx * (self.exp_sy_Ezx * self.Ezx[1:-1, 1:-1] + C * d_dy(self.Hx, self.dy))
        self.Ezy[1:-1, 1:-1] = self.exp_sx_Ezy * (self.exp_sx_Ezy * self.Ezy[1:-1, 1:-1] - C * d_dx(self.Hy, self.dx))

        self.Ez = self.Ezx + self.Ezy

        # Define the slit in the PEC boundary
        self.apply_PEC()

        # Incident wave
        # Ez[2:-2, -pml_width] += np.sin(omega * n_step * dt)

        # Update Hx and Hy (magnetic field components)
        self.Hx = self.exp_sy_Hx * (self.exp_sy_Hx * self.Hx + C * d_dy(self.Ez[1:-1, :], self.dy))
        self.Hy = self.exp_sx_Hy * (self.exp_sx_Hy * self.Hy - C * d_dx(self.Ez[:, 1:-1], self.dx))

        # Incident wave
        self.add_incident_wave()

        if is_DEBUG:
            end = timer()
            print(f"max |Ez|[{self.n_step}] = {abs(self.Ez).max():.5f} (calculation time {(end-start)*1000:.4f} ms)")

        self.I_out += self.Ez[self.out_pos, :] ** 2

    def update_1(self):
        self.n_step += 1
        if is_DEBUG:
            start = timer()

        C = self.dt/self.c
        # Update Ez (electric field component)
        self.Ezx[1:-1, 1:-1] = ((1 - self.sy_Ezx) * self.Ezx[1:-1, 1:-1] + C * d_dy(self.Hx, self.dy)) / (1 + self.sy_Ezx)
        self.Ezy[1:-1, 1:-1] = ((1 - self.sx_Ezy) * self.Ezy[1:-1, 1:-1] - C * d_dx(self.Hy, self.dx)) / (1 + self.sx_Ezy)

        self.Ez = self.Ezx + self.Ezy

        # Define the slit in the PEC boundary
        self.apply_PEC()

        # Incident wave
        # Ez[2:-2, -pml_width] += np.sin(omega * n_step * dt)

        # Update Hx and Hy (magnetic field components)
        self.Hx = ((1 - self.sy_Hx) * self.Hx + C * d_dy(self.Ez[1:-1, :], self.dy)) / (1 + self.sy_Hx)
        self.Hy = ((1 - self.sx_Hy) * self.Hy - C * d_dx(self.Ez[:, 1:-1], self.dx)) / (1 + self.sx_Hy)

        # Incident wave
        self.add_incident_wave()

        if is_DEBUG:
            end = timer()
            print(f"max |Ez|[{self.n_step}] = {abs(self.Ez).max():.5f} (calculation time {(end-start)*1000:.4f} ms)")

        self.I_out += self.Ez[self.out_pos, :] ** 2

    def add_incident_wave(self):
        # return
        wt = self.omega * self.n_step * self.dt
        ix = self.pml_width + 1
        self.Hy[ix, 2:-2] += np.sin(wt)
        # ix -= 1
        # self.Hy[ix, 2:-2] += np.sin(wt - self.k * self.dx)

    def init_wave(self, x_init):
        x_Ez = self.x[2:]
        cond = x_Ez < x_init
        self.Ezx[2:, 2:-2][cond, :] = np.sin(self.k * (x_Ez[cond][:, np.newaxis] - x_init))  # Sinusoidal wave in the x-direction
        x_Hy = (self.x[3:] + self.x[2:-1]) / 2
        cond = x_Hy < x_init
        self.Hy[2:, 1:-1][cond, :] = np.sin(self.k * (x_Hy[cond][:, np.newaxis] - x_init))  # Sinusoidal wave in the x-direction

    def start(self, N_cycles=300):
        self.n_step = 0
        self.init_fields()

        for _ in range(N_cycles):
            self.update()

    def get_x(self, show_PML=False):
        if show_PML:
            return self.x
        else:
            return self.x[self.pml_width:-self.pml_width]

    def get_y(self, show_PML=False):
        if show_PML:
            return self.y
        else:
            return self.y[self.pml_width:-self.pml_width]

    def get_out_intensity(self, show_PML=False):
        if show_PML:
            return self.I_out / self.n_step
        else:
            return self.I_out[self.pml_width:-self.pml_width] / self.n_step

    def get_Ez(self, show_PML=False):
        if show_PML:
            return self.Ez
        else:
            return self.Ez[self.pml_width:-self.pml_width, self.pml_width:-self.pml_width]

    def add_slit(self, slit_width, slit_height=0.5, slit_position=0):
        # Boundary conditions: Slit at x = slit_position, open at the middle
        slit_start_y = int((self.Ny - slit_width / self.dy) / 2)
        slit_end_y   = int((self.Ny + slit_width / self.dy) / 2)
        x_min = self.x.min()
        slit_start_x = int((slit_position - slit_height / 2 - x_min) / self.dx)
        slit_end_x   = int((slit_position + slit_height / 2 - x_min) / self.dx)

        def apply_PEC_slit(self):
            self.Ez[slit_start_x:slit_end_x, :slit_start_y] \
                = self.Ez[slit_start_x:slit_end_x, slit_end_y:] = 0

        self.apply_PEC = lambda self=self: apply_PEC_slit(self)
