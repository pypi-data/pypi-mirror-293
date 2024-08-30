import traceback
from dataclasses import asdict
from functools import partial, singledispatchmethod
from typing import Any, Callable, List, Literal, Tuple, Union

import numpy as np
import scipy.stats as sstats
from pydantic import Field
from pydantic.dataclasses import dataclass
from scipy import fftpack
from scipy.interpolate import interp1d
from scipy.signal import spectrogram
from scipy.spatial.transform import RotationSpline
from sklearn.decomposition import PCA

from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.time import TimeStep
from embdata.utils.import_utils import import_plt
from embdata.utils.plotting import plot_array, plot_varied
from embdata.utils.pretty import prettify


@dataclass
class Stats:
    mean: Any | None = None
    variance: Any | None = None
    skewness: Any | None = None
    kurtosis: Any | None = None
    min: Any | None = None
    max: Any | None = None
    lower_quartile: Any | None = None
    median: Any | None = None
    upper_quartile: Any | None = None
    non_zero_count: Any | None = None
    zero_count: Any | None = None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return prettify("Stats("
            f"mean={self.mean},"
            f"variance={self.variance},"
            f"skewness={self.skewness},"
            f"kurtosis={self.kurtosis},"
            f"min={self.min},"
            f"max={self.max},"
            f"lower_quartile={self.lower_quartile},"
            f"median={self.median},"
            f"upper_quartile={self.upper_quartile},"
            f"non_zero_count={self.non_zero_count},"
            f"zero_count={self.zero_count},"
            ")"
        )


    def __str__(self) -> str:
        return self.__repr__()


def stats(array: np.ndarray, axis=0, bias=True, sample_type: type[Sample] | None = None, sample_keys:  None | str | List[str] = None, **kwargs) -> Stats:
    """Compute statistics for an array along a given axis. Includes mean, variance, skewness, kurtosis, min, and max.

    Args:
      array (np.ndarray): The array to compute statistics for.
      axis (int, optional): The axis to compute statistics along. Defaults to 0.
      bias (bool, optional): Whether to use a biased estimator for the variance. Defaults to False.
      sample_type (type[Sample], optional): The type corresponding to a row in the array. Defaults to None.

    """
    stats_result = sstats.describe(array, axis=axis, bias=bias)
    mean = stats_result.mean
    variance = stats_result.variance
    skewness = stats_result.skewness
    kurtosis = stats_result.kurtosis
    min_val = np.min(array, axis=axis)
    max_val = np.max(array, axis=axis)
    lower_quartile = np.percentile(array, 25, axis=axis)
    median = np.percentile(array, 50, axis=axis)
    upper_quartile = np.percentile(array, 75, axis=axis)
    non_zero_count = np.count_nonzero(array, axis=axis)
    length = array.shape[axis]
    zero_count = length - non_zero_count
    
    stats_result = stats_result._asdict()
    stats_result["min"] = min_val
    stats_result["max"] = max_val
    stats_result["lower_quartile"] = lower_quartile
    stats_result["median"] = median
    stats_result["upper_quartile"] = upper_quartile
    stats_result["non_zero_count"] = non_zero_count
    stats_result["zero_count"] = zero_count
    stats_result["length"] = length
    if sample_type is not None:
        for k, v in stats_result.items():
            step = sample_type()
            for i, key in enumerate(sample_keys):

                try:
                    step[key] = step[key].__class__(v)
                except (TypeError, ValueError, AttributeError, KeyError):
                    step[key] = step[key].__class__.unflatten(v[i])
            stats_result[k] = step

    return Stats(**stats_result)


@dataclass
class Trajectory:
    """A trajectory of steps representing a time series of multidimensional data.

    This class provides methods for analyzing, visualizing, and manipulating trajectory data,
    such as robot movements, sensor readings, or any other time-series data.

    Attributes:
        steps (NumpyArray | List[Sample | NumpyArray]): The trajectory data.
        freq_hz (float | None): The frequency of the trajectory in Hz.
        keys (list[str] | None): The labels for each dimension of the trajectory.
        timestamps (NumpyArray | None): The time index of each step in the trajectory.
        angular_dims (list[int] | list[str] | None): The dimensions that are angular.

    Methods:
        plot: Plot the trajectory.
        map: Apply a function to each step in the trajectory.
        resample: Down sample or up sample the trajectory to a target frequency.
        frequencies: Plot the frequency spectrogram of the trajectory.
        frequencies_nd: Plot the n-dimensional frequency spectrogram of the trajectory.
        spectrogram: Plot the spectrogram of the trajectory.
        q01: Compute the 1st percentile of the trajectory.
        q99: Compute the 99th percentile of the trajectory.
        low_pass_filter: Apply a low-pass filter to the trajectory.
        stats: Compute statistics for the trajectory.
        transform: Apply a transformation to the trajectory.

    Example:
        >>> import numpy as np
        >>> from embdata.trajectory import Trajectory
        >>> # Create a simple 2D trajectory
        >>> steps = np.array([[0, 0], [1, 1], [2, 0], [3, 1], [4, 0]])
        >>> traj = Trajectory(steps, freq_hz=10, keys=["X", "Y"])
        >>> # Plot the trajectory
        >>> traj.plot().show()
        >>> # Compute and print statistics
        >>> print(traj.stats())
        >>> # Apply a low-pass filter
        >>> filtered_traj = traj.low_pass_filter(cutoff_freq=2)
        >>> filtered_traj.plot().show()
    """

    steps: NumpyArray | List[Sample | TimeStep] | Any = Field(
        description="A 2D array or list of samples representing the trajectory",
    )
    freq_hz: float | None = Field(default=None, description="The frequency of the trajectory in Hz")
    keys: List[str] | str | Tuple | None = Field(default=None, description="The labels for each dimension")
    timestamps: NumpyArray | None | List = Field(
        default=None,
        description="The timestamp of each step in the trajectory. Calculated if not provided.",
    )
    angular_dims: List[int] | List[str] | None = None
    _episode: Any | None = Field(default=None, description="The episode that the trajectory is part of.")
    _fig: Any | None = None
    _stats: Stats | None = None
    _sample_cls: type[Sample] | None = None
    _array: NumpyArray | None = None
    """Internal representation of the trajectory as a numpy array."""
    _map_unhistory: dict[str, Any] = Field(default_factory=dict)
    """The reverse of each transformation applied to the trajectory."""
    _map_unhistory_kwargs: dict[str, Any] = Field(default_factory=dict)
    """The keyword arguments for each reverse transformation applied to the trajectory."""
    _sample_keys: list[str] | None = None


    @property
    def array(self) -> np.ndarray:
        if self._array is None:
            if isinstance(self.steps[0], Sample):
                self._array = np.array([step.numpy() for step in self.steps])
            else:
                self._array = np.array(self.steps)
        return self._array

    def stats(self) -> Stats:
        """Compute statistics for the trajectory.

        Returns:
          dict: A dictionary containing the computed statistics, including mean, variance, skewness, kurtosis, min, and max.
        """
        if self._stats is None:
            self._stats = stats(self.array, axis=0, sample_type=self._sample_cls, sample_keys=self._sample_keys)
        return self._stats

    def plot(
        self,
        labels: list[str] | None = None,
        backend: Literal["matplotlib", "plotext"] = "plotext",
        varied: bool = False,
    ) -> "Trajectory":
        """Plot the trajectory. Saves the figure to the trajectory object. Call show() to display the figure.

        Args:
            labels (list[str], optional): The labels for each dimension of the trajectory. Defaults to None.
            time_step (float, optional): The time step between each step in the trajectory. Defaults to 0.1.
            backend (Literal["matplotlib", "plotext"], optional): The plotting backend to use. Defaults to "plotext".

        Returns:
          Trajectory: The original trajectory.

        """
        labels = labels or self.keys
        if varied:
            self._fig = plot_varied(self.array, labels, xstep=1 / self.freq_hz, backend=backend)
        else:
            self._fig = plot_array(self.array, labels, xstep=1 / self.freq_hz, backend=backend)
        return self

    def map(self, fn) -> "Trajectory":
        """Apply a function to each step in the trajectory.

        Args:
          fn: The function to apply to each step.

        Returns:
          Trajectory: The modified trajectory.
        """
        self._map_unhistory.setdefault(f"{fn.__name__ if hasattr(fn, __name__) else 'Map Function'}", []).append(
            lambda: self
        )
        return Trajectory(
            [fn(step) for step in self.steps],
            self.freq_hz,
            self.timestamps,
            self.keys,
            self.angular_dims,
            episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _sample_keys=self._sample_keys,
            _sample_cls=self._sample_cls,
        )

    def __len__(self):
        return len(self.steps)

    def __getitem__(self, index):
        return self.steps[index]

    def __iter__(self):
        return iter(self.steps)

    def __post_init__(self, *args, **kwargs):
        if args:
            self.steps = args[0]
        if len(args) > 1:
            self.freq_hz = args[1]
        if len(args) > 3:
            self.keys = args[3]
        if len(args) > 2:
            self.timestamps = args[2]
        if len(args) > 4:
            self.angular_dims = args[4]

        if "episode" in kwargs:
            self._episode = kwargs["episode"]
        elif "_episode" in kwargs:
            self._episode = kwargs["_episode"]
        if "_map_unhistory" in kwargs:
            self._map_unhistory = kwargs["_map_unhistory"]
        if "_map_unhistory_kwargs" in kwargs:
            self._map_unhistory_kwargs = kwargs["_map_unhistory_kwargs"]
        if "_sample_keys" in kwargs:
            self._sample_keys = kwargs["_sample_keys"]
        if "_sample_cls" in kwargs:
            self._sample_cls = kwargs["_sample_cls"]
        if "_fig" in kwargs:
            self._fig = kwargs["_fig"]
        if isinstance(self.steps[0], Sample):
            self._sample_cls = type(self.steps[0])
            self._sample_keys = self._sample_cls.keys()
        elif isinstance(self.steps[0], int | float | np.number):
            self.steps = [[step] for step in self.steps]
        if self.keys is None:
            self.keys = [f"Dimension {i}" for i in range(len(self.steps[0]))]
        if self.timestamps is None:
            self.timestamps = np.arange(0, len(self.array)) / self.freq_hz

        super(Trajectory).__init__(*args, **kwargs)

    def relative_to(self, new_origin_or_step_diff: int | np.ndarray = -1) -> "Trajectory":
        """Convert trajectory to be relative to a new origin. If new origin is an integer.

        Returns:
          Trajectory: The converted relative trajectory with one less step.
        """
        if isinstance(new_origin_or_step_diff, np.ndarray):
            return self._relative_to_state(new_origin_or_step_diff)
        self._map_unhistory.setdefault("absolute_from", []).append(partial(self.absolute_from, self.array[0]))
        return Trajectory(
            np.diff(self.array, n=-new_origin_or_step_diff, axis=0),
            self.freq_hz,
            self.keys,
            self.timestamps[1:],
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
        )


    def _relative_to_state(self, new_origin_or_step_diff: np.ndarray) -> "Trajectory":
        self._map_unhistory.setdefault("absolute_from", []).append(partial(self.absolute_from, new_origin_or_step_diff))
        return Trajectory(
            self.array - new_origin_or_step_diff,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def absolute_from(self, new_origin_value_or_index: None | np.ndarray | int = 0) -> "Trajectory":
        """Convert trajectory of relative actions to absolute actions.

        Can calculate from an initial state, origin, or index of the trajectory.

        Args:
          new_origin_or_value_index (np.ndarray): The initial state of the trajectory or index. Defaults to zeros.

        Returns:
          Trajectory: The converted absolute trajectory.
        """
        if new_origin_value_or_index is None:
            array = self._map_unhistory["absolute_from"].pop()().array
        else:
            self._map_unhistory.setdefault("relative_to", []).append(
                partial(self.relative_to, new_origin_or_step_diff=new_origin_value_or_index)
            )
            array = np.cumsum(np.concatenate([np.array([new_origin_value_or_index]), self.array], axis=0), axis=0)
        self._episode.freq_hz = self.freq_hz

        return Trajectory(
            array,
            self.freq_hz,
            self.keys,
            None,
            self.angular_dims,
            episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _sample_keys=self._sample_keys,
            _sample_cls=self._sample_cls,
        )

    def episode(self) -> Any:
        """Convert the trajectory to an episode."""
        if self._episode is None:
            msg = "This trajectory is not part of an episode"
            raise ValueError(msg)
        if len(self._episode.steps) != len(self.array):
            msg = "The trajectory and episode have different lengths"
            raise ValueError(msg)
        steps = []
        for step in self._episode.steps:
            for i, key in enumerate(self._sample_keys):
                try:
                    step[key] = step[key].__class__(self.array[i])
                except (TypeError, ValueError, AttributeError, KeyError):
                    step[key] = step[key].__class__.unflatten(self.array[i])

            steps.append(step)
        self._episode.steps = steps
        return self._episode

    def resample(self, target_hz: float) -> "Trajectory":
        if self.freq_hz is None:
            msg = "Cannot resample a trajectory without a frequency"
            raise ValueError(msg)
        if self.freq_hz == target_hz:
            return self
        if self.array.shape[0] == 0:
            msg = "Cannot resample an empty trajectory"
            raise ValueError(msg)

        # Calculate total duration
        total_duration = (len(self.array) - 1) / self.freq_hz

        # Calculate the number of samples in the resampled trajectory, ensuring to include the last sample
        num_samples = np.ceil(total_duration * target_hz) + 1

        # Generate resampled_time_idxs including the end of the duration
        resampled_time_idxs = np.linspace(0, total_duration, int(num_samples))

        if target_hz < self.freq_hz:
            # For downsampling, just take every nth sample.
            downsampling_factor = int(self.freq_hz / target_hz)
            resampled_array = self.array[::downsampling_factor, :]

        else:
            if len(self.array) < 4:
                msg = "Cannot upsample a trajectory with bicubic interpolationwith less than 4 samples"
                raise ValueError(msg)
            # Upsampling requires interpolation.
            num_dims = self.array.shape[1]
            resampled_array = np.zeros((len(resampled_time_idxs), num_dims))

            for i in range(num_dims):
                spline = interp1d(
                    np.arange(0, len(self.array)) / self.freq_hz,
                    self.array[:, i],
                    kind="cubic",
                    bounds_error=False,
                    fill_value="extrapolate",
                )
                resampled_array[:, i] = spline(resampled_time_idxs)

            if self.angular_dims:
                angular_dims = (
                    [self.keys.index(dim) for dim in self.angular_dims]
                    if isinstance(self.angular_dims[0], str)
                    else self.angular_dims
                )
                for i in angular_dims:
                    spline = RotationSpline(np.arange(0, len(self.array)) / self.freq_hz, self.array[:, i])
                    resampled_array[:, i] = spline(resampled_time_idxs)

        return Trajectory(
            resampled_array,
            target_hz,
            self.keys,
            resampled_time_idxs,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
        )

    def save(self, filename: str = "trajectory.png") -> "Trajectory":
        """Save the current figure to a file.

        Args:
          filename (str, optional): The filename to save the figure. Defaults to "trajectory.png".

        Returns:
          None
        """
        self._fig.savefig(filename)
        return self

    def show(self, backend: Literal["matplotlib", "plotext"] = "plotext") -> "Trajectory":
        """Display the current figure.

        Returns:
          None
        """
        if self._fig is None:
            msg = "No figure to show. Call plot() first."
            raise ValueError(msg)
        self._fig.show()

    def low_pass_filter(self, cutoff_freq: float) -> "Trajectory":
        """Apply a low-pass filter to the trajectory.

        Args:
          cutoff_freq (float): The cutoff frequency for the low-pass filter.

        Returns:
          Trajectory: The filtered trajectory.
        """
        fft = fftpack.fft(self.array, axis=0)
        frequencies = fftpack.fftfreq(len(fft), d=1.0 / self.freq_hz)
        fft[np.abs(frequencies) > cutoff_freq] = 0
        filtered_trajectory = fftpack.ifft(fft, axis=0)
        self._map_unhistory.setdefault("unlow_pass_filter", []).append(lambda: self)
        return Trajectory(
            np.real(filtered_trajectory),
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
        )

    def frequencies(self, backend: Literal["matplotlib", "plotext"] = "plotext") -> "Trajectory":
        plt = import_plt(backend)
        plt.clf()

        x = self.array
        N = x.shape[0]
        T = 1.0 / self.freq_hz
        freqs = np.fft.fftfreq(N, T)[: N // 2]
        fft_vals = np.fft.fft(x, axis=0)
        self._fig = plot_array(np.abs(fft_vals[0 : N // 2]), xstep=freqs[1] - freqs[0], backend=backend, title="Magnitude", xlabel="Frequency [Hz]") 
        self._map_unhistory.setdefault("unfrequencies", []).append(lambda: self)
        return Trajectory(
            np.abs(fft_vals[0 : N // 2]),
            self.freq_hz,
            [f"Frequency {key}" for key in self.keys],
            None,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def frequencies_nd(self, backend: Literal["matplotlib", "plotext"] = "plotext") -> "Trajectory":
        N = len(self.array)

        freqs = fftpack.fftfreq(N, d=1 / self.freq_hz)
        xstep = freqs[1] - freqs[0]
        Sxx = np.abs(fftpack.fftn(self.array))
        self._fig = plot_array(Sxx, xstep=xstep, backend=backend, title="Magnitude", xlabel="Frequency")
        return Trajectory(
            Sxx,
            self.freq_hz,
            self.keys,
            None,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )
        # keys = self.keys[:n_dims] if self.keys else [f"Dimension {i}" for i in range(n_dims)]

        # # Calculate the number of rows and columns for subplots
        # n_rows = (n_dims + 1) // 2  # +1 to round up
        # n_cols = 2

        # plt.subplots(n_rows, n_cols)
        # plt.theme("fhd")

        # for i in range(n_dims):
        #     row = i // n_cols + 1
        #     col = i % n_cols + 1
        #     plt.subplot(row, col)
        #     plt.plot(freqs, Sxx[:, i])
        #     plt.title(f"{keys[i]} ND Frequency")
        #     plt.xlabel("Frequency [Hz]")
        #     plt.ylabel("Magnitude")
        #     plt.xlim(0, self.freq_hz / 2)
        #     plt.ylim(np.min(Sxx), np.max(Sxx))
        # # If there's an odd number of dimensions, add a blank subplot
        # if n_dims % 2 != 0:
        #     plt.subplot(n_rows, n_cols)
        #     plt.title("Unused subplot")

        # self._fig = plt
        # return self

    def spectrogram(self, backend: Literal["matplotlib", "plotext"] = "plotext") -> "Trajectory":
        plt = import_plt(backend)
        plt.clf()
        plt.cld()
        x = self.array
        fs = self.freq_hz
        f, t, Sxx = spectrogram(x, fs)
        self._fig = plot_array(Sxx, xstep=1 / fs, backend=backend, title="Spectrogram", xlabel="Time")
        return Trajectory(
            Sxx,  
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def q01(self) -> float:
        return np.percentile(self.array, 1, axis=0)

    def q99(self) -> float:
        return np.percentile(self.array, 99, axis=0)

    def mean(self) -> np.ndarray | Sample:
        return np.mean(self.array, axis=0)

    def variance(self) -> np.ndarray | Sample:
        return np.var(self.array, axis=0)

    def std(self) -> float:
        return np.std(self.array, axis=0)

    def skewness(self) -> float:
        return self.stats().skewness

    def kurtosis(self) -> float:
        return self.stats().kurtosis

    def min(self) -> float:
        return self.stats().min

    def max(self) -> float:
        return self.stats().max

    def lower_quartile(self) -> float:
        return self.stats().lower_quartile

    def median(self) -> float:
        return self.stats().median

    def upper_quartile(self) -> float:
        return self.stats().upper_quartile

    def non_zero_count(self) -> float:
        return self.stats().non_zero_count

    def zero_count(self) -> float:
        return self.stats().zero_count

    def pca(self, whiten=False) -> "Trajectory":
        """Apply PCA normalization to the trajectory.

        Returns:
          Trajectory: The PCA-normalized trajectory.
        """
        pca: PCA = PCA(n_components=self.array.shape[1], whiten=whiten)
        self._map_unhistory.setdefault("unpca", []).append(partial(self.unpca, pca))
        self._map_unhistory_kwargs.setdefault("unpca", []).append({"pca": pca})
        array =  pca.fit_transform(self.array)
        self._fig = plot_array(array, xstep=1 / self.freq_hz, labels=[f"PCA {i}" for i in range(array.shape[1])],
                                 title="PCA Normalized Trajectory")
        return Trajectory(
            array,
            self.freq_hz,
            [f"PCA {i}" for i in range(array.shape[1])],
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def unpca(self, pca_model=None) -> "Trajectory":
        """Reverse PCA normalization on the trajectory.

        Returns:
          Trajectory: The original trajectory before PCA normalization.
        """
        if pca_model is None:
            pca_model: PCA = self._map_unhistory_kwargs["unpca"].pop()["pca"]
            original_array = pca_model.inverse_transform(self.array)
        else:
            original_array = pca_model.inverse_transform(self.array)
        return Trajectory(
            original_array,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def standardize(self) -> "Trajectory":
        """Apply standard normalization to the trajectory.

        Returns:
          Trajectory: The standardized trajectory.
        """
        mean = np.mean(self.array, axis=0)
        std = np.std(self.array, axis=0)
        self._map_unhistory.setdefault("unstandardize", []).append(partial(self.unstandardize, mean, std))
        self._map_unhistory_kwargs.setdefault("unstandardize", []).append(
            {
                "mean": mean,
                "std": std,
            },
        )
        self._fig = plot_array((self.array - mean) / std, xstep=1 / self.freq_hz, backend="plotext", title="Standardized Trajectory")
        return Trajectory(
            (self.array - mean) / std,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def unstandardize(self, mean: np.ndarray | None = None, std: np.ndarray | None = None) -> "Trajectory":
        """Reverse standard normalization on the trajectory. Call with no arguments to use the last mean and std.

        NOTE: If the trajectory was not standardized, the mean and std must be provided.
        """
        if mean is None and std is not None or mean is not None and std is None:
            msg = "Both mean and std must be provided or omitted"
            raise ValueError(msg)
        if mean is None and "undstandardize" not in self._map_unhistory or not self._map_unhistory["unstandardize"]:
            msg = "No mean and std provided and no standardization found in history"
            raise ValueError(msg)

        array = self._map_unhistory["unstandardize"].pop()() if mean is None else self.array * std + mean
        steps = [self._sample_cls(step) for step in array] if self._sample_cls is not None else array
        return Trajectory(
            steps,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
        )

    def minmax(self, min: float = 0, max: float = 1) -> "Trajectory":
        """Apply min-max normalization to the trajectory.

        Args:
          min (float, optional): The minimum value for the normalization. Defaults to 0.
          max (float, optional): The maximum value for the normalization. Defaults to 1.

        Returns:
          Trajectory: The normalized trajectory.
        """
        min_vals = np.min(self.array, axis=0)
        max_vals = np.max(self.array, axis=0)
        self._map_unhistory.setdefault("unminmax", []).append(partial(self.unminmax))
        self._map_unhistory_kwargs.setdefault("unminmax", []).append(
            {
                "orig_min": min_vals,
                "orig_max": max_vals,
            },
        )
        array = (self.array - min_vals) / (max_vals - min_vals) * (max - min)
        self._fig = plot_array(array, xstep=1 / self.freq_hz, backend="plotext", title="Min-Max Normalized Trajectory")
        return Trajectory(
            array,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )

    def unminmax(
        self,
        orig_min: np.ndarray | Sample | None = None,
        orig_max: np.ndarray | Sample | None = None,
    ) -> "Trajectory":
        """Reverse min-max normalization on the trajectory."""
        if orig_min is None and orig_max is not None or orig_min is not None and orig_max is None:
            msg = "Both orig_min and orig_max must be provided or omitted"
            raise ValueError(msg)
        if orig_min is None and "unminmax" not in self._map_unhistory or not self._map_unhistory["unminmax"]:
            msg = "No orig_min and orig_max provided and no minmax normalization found in history"
            raise ValueError(msg)
        if orig_min is None:
            return self._map_unhistory["unminmax"].pop()()
        norm_min = np.min(self.array, axis=0)
        norm_max = np.max(self.array, axis=0)
        array = (self.array - norm_min) / (norm_max - norm_min) * (orig_max - orig_min) + orig_min
        steps = [self._sample_cls(step) for step in array] if self._sample_cls is not None else array
        return Trajectory(
            steps,
            self.freq_hz,
            self.keys,
            self.timestamps,
            self.angular_dims,
            _sample_cls=self._sample_cls,
            _sample_keys=self._sample_keys,
            _episode=self._episode,
            _map_unhistory=self._map_unhistory,
            _map_unhistory_kwargs=self._map_unhistory_kwargs,
            _fig=self._fig,
        )


def main() -> None:
    from datasets import Dataset, load_dataset

    from embdata.motion.control import HandControl

    ds = Dataset.from_list(
        list(
            load_dataset("mbodiai/oxe_bridge", "default", split="default", streaming=True)
            .take(100)
            .filter(lambda x: x["episode_idx"] == 1),
        ),
    )

    ds = np.array([HandControl(**a["action"]).numpy() for a in ds])
    trajectory = Trajectory(
        ds,
        freq_hz=5,
        keys=[
            "X",
            "Y",
            "Z",
            "Roll",
            "Pitch",
            "Yaw",
            "Grasp",
        ],
        angular_dims=["Roll", "Pitch", "Yaw"],
    )
    trajectory.spectrogram().save("spectrogram.png")
    trajectory.plot().save("trajectory.png")
    trajectory.frequencies_nd().save("nd_spectrogram.png")
    trajectory.resample(5).spectrogram().save("resampled_trajectory.png")
    trajectory.resample(5).plot().save("resampled_trajectory_plot.png")


if __name__ == "__main__":
    main()
