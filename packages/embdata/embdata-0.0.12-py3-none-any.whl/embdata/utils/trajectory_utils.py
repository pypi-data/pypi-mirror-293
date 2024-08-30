import matplotlib.pyplot as plt
import numpy as np
from lager import log


def DTWDistance(s, t, w):
    n = len(s)
    m = len(t)

    # Adjust the window size based on the difference in length between the sequences
    w = max(w, abs(n - m))

    # Initialize the DTW matrix with infinity
    DTW = np.full((n + 1, m + 1), np.inf)
    DTW[0, 0] = 0

    # Populate the matrix within the window
    for i in range(1, n + 1):
        for j in range(max(1, i - w), min(m, i + w) + 1):
            DTW[i, j] = 0

    # Compute the DTW distance
    for i in range(1, n + 1):
        for j in range(max(1, i - w), min(m, i + w) + 1):
            cost = abs(s[i - 1] - t[j - 1])  # Example cost function (absolute difference)
            DTW[i, j] = cost + min(
                DTW[i - 1, j],  # insertion
                DTW[i, j - 1],  # deletion
                DTW[i - 1, j - 1],
            )  # match

    return DTW[n, m]

if __name__ == "__main__":
  # Example usage
  s = [1, 2, 3, 4, 2, 3]
  t = [1, 2, 3, 3, 4, 5]
  w = 1

  distance = DTWDistance(s, t, w)
  log.info("DTW Distance:", distance)


  def plot_warping_path(s, t, DTW):
      n, m = len(s), len(t)
      i, j = n, m
      path = [(i, j)]

      while i > 0 and j > 0:
          if i == 0:
              j -= 1
          elif j == 0:
              i -= 1
          else:
              min_idx = np.argmin([DTW[i - 1, j], DTW[i, j - 1], DTW[i - 1, j - 1]])
              if min_idx == 0:
                  i -= 1
              elif min_idx == 1:
                  j -= 1
              else:
                  i -= 1
                  j -= 1
          path.append((i, j))

      path = path[::-1]

      plt.figure(figsize=(10, 10))
      plt.imshow(DTW, interpolation="nearest", cmap="Blues")
      plt.plot([p[1] for p in path], [p[0] for p in path], "r")
      plt.xlabel("Sequence t")
      plt.ylabel("Sequence s")
      plt.title("DTW Cost Matrix with Optimal Warping Path")
      plt.colorbar()
      plt.savefig("dtw.png")


  # Example usage
  s = [1, 2, 3, 4, 2, 3]
  t = [1, 2, 3, 3, 4, 5]
  w = 1

  # Calculate DTW matrix
  DTW = np.full((len(s) + 1, len(t) + 1), np.inf)
  DTW[0, 0] = 0
  for i in range(1, len(s) + 1):
      for j in range(max(1, i - w), min(len(t), i + w) + 1):
          cost = abs(s[i - 1] - t[j - 1])
          DTW[i, j] = cost + min(DTW[i - 1, j], DTW[i, j - 1], DTW[i - 1, j - 1])

  plot_warping_path(s, t, DTW)
