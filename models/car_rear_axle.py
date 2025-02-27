#!/usr/bin/env python3
import numpy as np

class Car:
    """
    Kinematic model of a car-like robot with ref point on rear axle
    States: x, y, yaw, v
    Inputs: a, delta
    """
    def __init__(self, x=0, y=0, yaw=0, v=0, delta=0, a=0, L=3, a_max=2, delta_max=np.pi/4):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.delta = delta
        self.a = a

        self.L = L # m
        self.a_max = a_max # m/s^2
        self.delta_max = delta_max # rad

    def _update_controls(self, a, delta):
        self.a = np.fmin(np.fmax(a, -self.a_max), self.a_max)
        self.delta = np.fmin(np.fmax(delta, -self.delta_max), self.delta_max)

    def model(self, a, delta):
        self._update_controls(a, delta)

        state_dot = np.array([0., 0., 0., 0.])
        state_dot[0] = self.v * np.cos(self.yaw)
        state_dot[1] = self.v * np.sin(self.yaw)
        state_dot[2] = self.v * np.tan(self.delta) / self.L
        state_dot[3] = self.a

        return state_dot

    def step(self, a, delta, dt):
        state_dot = self.model(a, delta)
        state = self.get_state()
        self.set_state(state + state_dot * dt)

    def get_state(self):
        state = np.array([0., 0., 0., 0.])
        state[0] = self.x
        state[1] = self.y
        state[2] = self.yaw
        state[3] = self.v

        return state

    def set_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.yaw = state[2]
        self.v = state[3]
