try:
    # pip install cupy-cuda12x
    import cupy as cp
    # Check if CUDA is available
    if cp.cuda.is_available():
        xp = cp
        print("CUDA is available. Using CuPy.")
    else:
        raise ImportError("CUDA is not available. Falling back to NumPy.")
except ImportError as e:
    print(e)
    import numpy as np
    xp = np
    print("Using NumPy.")

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
from timeit import default_timer as timer
from math import ceil


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
    return xp.diff(u, axis=0) / dx


def d_dy(u, dy):
    return xp.diff(u, axis=1) / dy


class EM2D:
    def __init__(self, Lx=20., Ly=20., Nx=200, Ny=201, wavelength=3, exponential_PML: bool=True):
        """
        Object constuctor
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        :param wavelength: is the wavelength of the incoming wave.
        :param exponential_PML: selecting a PML update scheme
        """
        self.exponential_PML = exponential_PML

        # function to apply PEC condition (for example, a slit)
        self.apply_PEC = lambda: None

        # field components
        self.Ezx = None
        self.Ezy = None
        self.Ez = None
        self.Hx = None
        self.Hy = None
        self.I_tmp = 0
        self.I_out = None
        # domain parameters
        self.Lx = None
        self.Ly = None
        self.Nx = None
        self.Ny = None
        self.dx = None
        self.dy = None
        self.x = None
        self.y = None
        # time parameters
        self.Nt = None #  number of cycles in one period of the incoming wave
        self.dt = None
        # PML parameters
        self.pml_width = None
        self.sigma_max = None
        self.pml_p = None
        # PML coefficient for the fields calculations
        self.exp_sy_Ezx = None
        self.exp_sx_Ezy = None
        self.exp_sy_Hx = None
        self.exp_sx_Hy = None
        self.sy_Ezx = None
        self.sx_Ezy = None
        self.sy_Hx = None
        self.sx_Hy = None
        # Incoming wave parameters
        self.wavelength = None
        self.k = None
        self.omega = None
        # Wave velocity
        self.c = 1
        # time step
        self.n_step = 0

        self.init_domain(Lx, Ly, Nx, Ny)
        self.create_grid()
        self.set_PML()
        self.init_PML()

        self.set_wavelength(wavelength, update_dt=True)

        # self.init_fields()
        self.out_pos = -self.pml_width - 2

        # for extern accumulations
        self.accumulator = 0

    def norm(self, field):
        return xp.linalg.norm(field - self.accumulator)
        
    def set_wavelength(self, wavelength, update_dt: bool=True):
        """
        Set the wavelength for incoming wave
        :param wavelength: is the wavelength of the incoming wave.
        :param update_dt: updating the time step relative to one period of the incoming wave and taking into account the Courant condition
        """
        # Wavelength of the incident wave
        self.wavelength = wavelength
        # λ = c / f -> f = c / λ
        # Wave number
        self.k = 2 * xp.pi / self.wavelength
        # Angular frequency
        self.omega = self.c * self.k

        if update_dt:
            # T = λ / c
            T = self.wavelength / self.c
            dt0 = 0.75 * self.Courant()
            self.Nt = ceil(T / dt0)
            self.dt = T / self.Nt
            # print(f"{self.dt/self.Courant()}")

    def init_domain(self, Lx, Ly, Nx, Ny):
        """
        Init domain
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        """
        # domain size
        self.Lx = Lx
        self.Ly = Ly

        # number of grid points
        self.Nx = Nx
        self.Ny = Ny

        self.dx = self.Lx / self.Nx  # grid spacing in x direction
        self.dy = self.Ly / self.Ny  # grid spacing in y direction

    def Courant(self):
        """
        The convergence condition by Courant–Friedrichs–Lewy (stability criterion of difference scheme)
        :return: time step
        """
        return 1 / xp.sqrt(1 / self.dx ** 2 + 1 / self.dy ** 2)

    def set_PML(self, pml_width=20, sigma_max=1, pml_p: int=2):
        """
        Init PML parameters
        :param pml_width: is the number of points used for the PML width
        :param sigma_max: is the maximum sigma value for PML (in  1 / dt units)
        :param pml_p: is the order of sigma function
        """
        self.pml_width = pml_width
        self.sigma_max = sigma_max
        self.pml_p = pml_p

    def init_PML(self):
        """
        Init PML
        """
        # PML damping profiles
        sigma_x = xp.zeros(self.Nx)
        sigma_y = xp.zeros(self.Ny)
        sigma_Hx = xp.zeros(self.Nx - 1)
        sigma_Hy = xp.zeros(self.Ny - 1)

        i_pml = xp.arange(1, self.pml_width+1)
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

        C = 1 / 2 # in dt units
        sy_Ezx = sigma_y[xp.newaxis, 1:-1] * C
        sx_Ezy = sigma_x[1:-1, xp.newaxis] * C
        sy_Hx = sigma_Hy[xp.newaxis, :] * C
        sx_Hy = sigma_Hx[:, xp.newaxis] * C

        if self.exponential_PML:
            self.exp_sy_Ezx = xp.exp(-sy_Ezx)
            self.exp_sx_Ezy = xp.exp(-sx_Ezy)
            self.exp_sy_Hx = xp.exp(-sy_Hx)
            self.exp_sx_Hy = xp.exp(-sx_Hy)
        else:
            self.sy_Ezx = sy_Ezx
            self.sx_Ezy = sx_Ezy
            self.sy_Hx = sy_Hx
            self.sx_Hy = sx_Hy

    def init_fields(self):
        """
        Init fields
        """
        self.n_step = 0

        # z-component of the electric field (1)
        self.Ezx = xp.zeros((self.Nx, self.Ny))
        # z-component of the electric field (2)
        self.Ezy = xp.zeros((self.Nx, self.Ny))
        self.Ez = self.Ezx + self.Ezy

        # x-component of the magnetic field
        self.Hx = xp.zeros((self.Nx-2, self.Ny-1))
        # y-component of the magnetic field
        self.Hy = xp.zeros((self.Nx-1, self.Ny-2))

        # field intensity along the x-axis
        self.I_out = xp.zeros((self.Nx-1, ))

    def create_grid(self):
        """
        Create grid
        """
        self.x = xp.linspace(-self.Lx/2, self.Lx/2, self.Nx)
        self.y = xp.linspace(-self.Ly/2, self.Ly/2, self.Ny)
        # X, Y = xp.meshgrid(x, y, indexing="ij")

    def update(self):
        """
        Updating fields over time (one simulation cycle).
        """
        self.n_step += 1
        if is_DEBUG:
            start = timer()

        C = self.dt/self.c

        # Update Ez (electric field component)
        if self.exponential_PML:
            self.Ezx[1:-1, 1:-1] = self.exp_sy_Ezx * (self.exp_sy_Ezx * self.Ezx[1:-1, 1:-1] + C * d_dy(self.Hx, self.dy))
            self.Ezy[1:-1, 1:-1] = self.exp_sx_Ezy * (self.exp_sx_Ezy * self.Ezy[1:-1, 1:-1] - C * d_dx(self.Hy, self.dx))
        else:
            self.Ezx[1:-1, 1:-1] = ((1 - self.sy_Ezx) * self.Ezx[1:-1, 1:-1]
                                    + C * d_dy(self.Hx, self.dy)) / (1 + self.sy_Ezx)
            self.Ezy[1:-1, 1:-1] = ((1 - self.sx_Ezy) * self.Ezy[1:-1, 1:-1]
                                    - C * d_dx(self.Hy, self.dx)) / (1 + self.sx_Ezy)

        self.Ez = self.Ezx + self.Ezy

        # Define the slit in the PEC boundary
        self.apply_PEC()

        # Incident wave
        # Ez[2:-2, -pml_width] += xp.sin(omega * n_step * dt)

        # Update Hx and Hy (magnetic field components)
        if self.exponential_PML:
            self.Hx = self.exp_sy_Hx * (self.exp_sy_Hx * self.Hx + C * d_dy(self.Ez[1:-1, :], self.dy))
            self.Hy = self.exp_sx_Hy * (self.exp_sx_Hy * self.Hy - C * d_dx(self.Ez[:, 1:-1], self.dx))
        else:
            self.Hx = ((1 - self.sy_Hx) * self.Hx + C * d_dy(self.Ez[1:-1, :], self.dy)) / (1 + self.sy_Hx)
            self.Hy = ((1 - self.sx_Hy) * self.Hy - C * d_dx(self.Ez[:, 1:-1], self.dx)) / (1 + self.sx_Hy)

        # Incident wave
        self.add_incident_wave()

        if is_DEBUG:
            end = timer()
            print(f"max |Ez|[{self.n_step}] = {abs(self.Ez).max():.5f} (calculation time {(end-start)*1000:.4f} ms)")

        self.I_tmp += self.Ez[self.out_pos, :] ** 2
        if self.n_step % self.Nt == 0:
            self.I_out = self.I_tmp / self.Nt
            self.I_tmp = 0

    def add_incident_wave(self):
        # return
        wt = self.omega * self.n_step * self.dt
        ix = self.pml_width + 1
        self.Hy[ix, 2:-2] += xp.sin(wt)

    def init_wave(self, x_init):
        x_Ez = self.x[2:]
        cond = x_Ez < x_init
        self.Ezx[2:, 2:-2][cond, :] = xp.sin(self.k * (x_Ez[cond][:, xp.newaxis] - x_init))  # Sinusoidal wave in the x-direction
        x_Hy = (self.x[3:] + self.x[2:-1]) / 2
        cond = x_Hy < x_init
        self.Hy[2:, 1:-1][cond, :] = xp.sin(self.k * (x_Hy[cond][:, xp.newaxis] - x_init))  # Sinusoidal wave in the x-direction

    def do_n(self, N_cycles, accumulate: bool = False):
        """
        Performing N_cycles simulation cycles.
        :accumulate: perform accumulation of the absolute value of the Poynting vector
        """
        S = 0
        for _ in range(N_cycles):
            self.update()
            if accumulate:
                S += self.get_S()
        return S / N_cycles  # Yield the final accumulated value after the last cycle

    def start_until(self, N_cycles=300):
        """
        Performing simulations until fields saturation
        :return: absolute value of the Poynting vector
        """
        # clear previous simulations
        self.init_fields()

        if N_cycles is not None:
            self.do_n(N_cycles)
        else:
            # number of cycles for wave propagation along the x-axis from the start to the end of calculation area
            N_t = ceil(2 * (self.Lx - 2 * self.dx * self.pml_width) / self.wavelength)

            self.do_n(N_t * self.Nt)
            return self.do_n(self.Nt, accumulate=True)

    def get_x(self, show_PML: bool=False):
        """
        Get the x coordinates
        :param show_PML: with or without the PML region
        """
        if show_PML:
            out = self.x
        else:
            out = self.x[self.pml_width:-self.pml_width]
        if isinstance(out, cp.ndarray):
            return out.get()
        else:
            return out

    def get_y(self, show_PML: bool=False):
        """
        Get the y coordinates
        :param show_PML: with or without the PML region
        """
        if show_PML:
            out = self.y
        else:
            out = self.y[self.pml_width:-self.pml_width]
        if isinstance(out, cp.ndarray):
            return out.get()
        else:
            return out

    def get_out_intensity(self, show_PML: bool=False):
        if show_PML:
            out = self.I_out
        else:
            out = self.I_out[self.pml_width:-self.pml_width]
        if isinstance(out, cp.ndarray):
            return out.get()
        else:
            return out

    def get_Ez(self, show_PML: bool=False):
        """
        Get the z-component of the electric field
        :param show_PML: with or without the PML region
        """
        if show_PML:
            out = self.Ez
        else:
            out = self.Ez[self.pml_width:-self.pml_width, self.pml_width:-self.pml_width]
        if isinstance(out, cp.ndarray):
            return out.get()
        else:
            return out

    def get_Sx(self, show_PML: bool=False):
        """
        Get the x-component of the Poynting vector
        :param show_PML: with or without the PML region
        """
        if show_PML:
            return -self.Ez[1:-1, 1:-1] * (self.Hy[1:, :] + self.Hy[:-1, :]) / 2
        else:
            return -self.Ez[self.pml_width+1:-self.pml_width-1, self.pml_width+1:-self.pml_width-1]\
                   * (self.Hy[self.pml_width+1:-self.pml_width, self.pml_width:-self.pml_width]
                      + self.Hy[self.pml_width:-self.pml_width-1, self.pml_width:-self.pml_width]) / 2

    def get_Sy(self, show_PML: bool=False):
        """
        Get the y-component of the Poynting vector
        :param show_PML: with or without the PML region
        """
        if show_PML:
            return self.Ez[1:-1, 1:-1] * (self.Hx[:, 1:] + self.Hx[:, -1]) / 2
        else:
            return self.Ez[self.pml_width+1:-self.pml_width-1, self.pml_width+1:-self.pml_width-1]\
                   * (self.Hx[self.pml_width:-self.pml_width, self.pml_width+1:-self.pml_width]
                      + self.Hx[self.pml_width:-self.pml_width, self.pml_width:-self.pml_width-1]) / 2

    def get_S(self, show_PML: bool=False):
        """
        Get the absolute value of the Poynting vector
        :param show_PML: with or without the PML region
        """
        out = xp.sqrt(self.get_Sx(show_PML)**2 + self.get_Sy(show_PML)**2)
        if isinstance(out, cp.ndarray):
            return out.get()
        else:
            return out

    def add_slit(self, width, height=0.5, position=0, apply_PEC=None):
        """
        Adding single slit
        :param width: is the slit width
        :param height: is the slit height (the screen thickness)
        :param position: is the x-position of the screen with the slit
        :param apply_PEC: is the external function to apply PEC
        """
        # Boundary conditions: Slit at x = slit_position, open at the middle
        slit_start_y = int((self.Ny - width / self.dy) / 2)
        slit_end_y   = int((self.Ny + width / self.dy) / 2)
        x_min = self.x.min()
        slit_start_x = int((position - height / 2 - x_min) / self.dx)
        slit_end_x   = int((position + height / 2 - x_min) / self.dx)

        if apply_PEC is None:
            def apply_PEC_slit(self):
                self.Ez[slit_start_x:slit_end_x, :slit_start_y] \
                    = self.Ez[slit_start_x:slit_end_x, slit_end_y:] = 0
            self.apply_PEC = lambda self=self: apply_PEC_slit(self)
        else:
            self.apply_PEC = apply_PEC
