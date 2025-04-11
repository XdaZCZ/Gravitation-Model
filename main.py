import math as mt
import maths as ms
import plotly.express as px

# constants
gravitational_constant = 6.6743e-11  # meter cubed  per kilogram per second squared
start_point = (1100, 600)  # meters
start_velocity = (-1, 2)  # meter per second
mass = 2e14  # kilograms
dt = 0.05  # seconds
limit_t = 5000  # seconds
sampling = 1000  # 1 out of sampling (e.g. 100) will be displayed in plot
isOrbital = True  # if True automatically calculates orbital vel
factor = 1  # a coefficient for orbital speed

# calculated constants
grav_parameter = mass * gravitational_constant  # meter cubed per second squared
r_0 = 1 / mt.sqrt(pow(start_point[0], 2) + pow(start_point[1], 2))
orbital_speed = mt.sqrt(grav_parameter * r_0)
orbital_vel = ms.multiply(
    orbital_speed * r_0,
    [-start_point[1], start_point[0]],
)
period = 2 * mt.pi / r_0 / orbital_speed

print("Orbital speed for circular orbit with current conditions: " + str(orbital_speed))
print("Period for circular orbit with current conditions: " + str(period))


def prepare() -> list:
    # mass
    mass_list = list(str(int(mass)))
    mass_string = "{0},{1}{2}e{3}".format(
        mass_list[0], mass_list[1], mass_list[2], len(mass_list) - 1
    )
    # initial velocity
    if isOrbital and factor == 1:
        vel = orbital_vel
    elif isOrbital and factor != 1:
        vel = ms.multiply(
            orbital_speed * r_0 * factor,
            [-start_point[1], start_point[0]],
        )
    else:
        vel = start_velocity
    vel_round = [round(vel[0], 2), round(vel[1], 2)]
    return [mass_string, vel_round]


# main part of the code, calculates the points
def move(isOrbital: bool, factor: int) -> list:
    t = 0  # total time run
    mark = 0  # marks how manz points to skip before adding one to the points_list
    points_list = []  # collects all the points to be displayed [[x1,y1],[x2,y2]...]
    while t < limit_t:
        if t != 0:
            point = point_future
            point_future = 0
            vel_now = vel_future
            vel_future = 0
        else:
            point = ms.copy(start_point)
            if isOrbital and factor == 1:
                vel_now = ms.copy(orbital_vel)
            elif isOrbital and factor != 1:
                eliptic_vel = ms.multiply(
                    orbital_speed * r_0 * factor,
                    [-start_point[1], start_point[0]],
                )
                vel_now = ms.copy(eliptic_vel)
            else:
                vel_now = ms.copy(start_velocity)

        if mark == 0:
            points_list.append(point)
            mark = sampling
        else:
            mark -= 1

        condition = pow(point[0], 2) + pow(point[1], 2) > 169 * mass * pow(
            10, -10
        )  # condition to switch between dt=0.05 and dt=0.001
        if condition:
            point_future = ms.point_calc(dt, point, vel_now)
            vel_future = ms.velocity(grav_parameter, dt, point, vel_now)
            t += dt
        else:
            point_future = ms.point_calc(dt / 50, point, vel_now)
            vel_future = ms.velocity(grav_parameter, dt / 50, point, vel_now)
            t += dt / 50
    return points_list


# active part of the code, in the end shows the plot
points_list = move(isOrbital, factor)
prep = prepare()
coords = ms.sort(points_list)
fig = px.scatter(x=coords[0], y=coords[1], labels={"x": "x / m", "y": "y / m"})
fig.update_layout(
    width=800,
    height=800,
    title="mass: {0}, Starting point: {1}, Initial velocity: {2}".format(
        prep[0], start_point, prep[1]
    ),
)
fig.update_yaxes(scaleanchor="x", scaleratio=1)
fig.show()
