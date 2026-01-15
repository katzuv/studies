import matplotlib.pyplot as plt
import numpy as np
import scipy

gravity = 9.81
length = 0.981
time_frame = (0, 10)


def pendulum_ode(t, y):
    theta, omega = y
    second_derivative = -(gravity / length) * np.sin(theta)
    return np.array((omega, second_derivative))


if __name__ == "__main__":
    initial_condition = (1, 2, 2.5, 2.75, 3)
    for ic in initial_condition:
        sol = scipy.integrate.solve_ivp(
            pendulum_ode,
            time_frame,
            (ic, 0),
            t_eval=np.linspace(0, 10, 1000),
            rtol=1e-9,  # Reducing allowed errors.
            atol=1e-9,
        )

        time, theta = sol.t, sol.y[0]
        (line,) = plt.plot(time, theta, label=f"$\\theta_0$: {ic} rad")
        color = line.get_color()

        minima_indices = scipy.signal.argrelextrema(theta, np.less)[0]
        plt.scatter(
            time[minima_indices],
            theta[minima_indices],
            color=color,
            marker="^",
            s=50,
            zorder=5,
        )

        for count, index in enumerate(minima_indices):
            x_pos = time[index]
            y_pos = theta[index]

            plt.text(
                x_pos,
                y_pos + 0.4,
                str(count + 1),
                color=color,
                ha="center",
                va="top",
                fontweight="bold",
            )

    plt.xlabel("Time (s)")
    plt.grid()
    plt.legend()
    plt.ylabel("Angular Displacement (rad)")
    plt.savefig("pendulum_ode.svg", format="svg")
    plt.show()
