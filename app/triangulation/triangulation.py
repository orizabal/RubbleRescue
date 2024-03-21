import numpy as np
from scipy.optimize import minimize
from scipy.io.wavfile import read
from typing import List
from .gcc_phat import gcc_phat 
from models import AudioItem, Module
from dao import DaoFactory

MIC_DISTANCE = 0.23
MAX_TDOA = MIC_DISTANCE / 343.2
SAMPLE_RATE = 16000

def _audioToNpArray(audioItems: List[AudioItem]):
    signals = []
    for item in audioItems:
        audio = read(item.ref)
        signals.append(np.array(audio[1], dtype=np.int16))
    
    return signals


def _get_direction(signals):
    # calling gcc_phat function to calculate TDOA between each pair defined
    tau12, _ = gcc_phat(signals[0], signals[1], fs=SAMPLE_RATE, max_tau=MAX_TDOA, interp=1)
    tau13, _ = gcc_phat(signals[0], signals[2], fs=SAMPLE_RATE, max_tau=MAX_TDOA, interp=1)
    tau23, _ = gcc_phat(signals[1], signals[2], fs=SAMPLE_RATE, max_tau=MAX_TDOA, interp=1)
    
    # call DOA calculation function
    doa = _calculate_doa(tau12, tau13, tau23, MIC_DISTANCE)
    return doa


# calculate DOA based on single TDOA value
def _calculate_doa(tau12, tau13, tau23, mic_distance, sound_speed=343.2):
        # Convert TDOAs to distance differences
        d1 = mic_distance 
        d2 = d1 - tau12 * sound_speed
        d3 = d1 - tau13 * sound_speed

        # Microphone positions
        M1 = np.array([0, 0])
        M2 = np.array([mic_distance, 0])
        M3 = np.array([mic_distance / 2, mic_distance * np.sqrt(3) / 2])

        # objective function: sum of squared differences between expected and actual distances
        def objective_function(S):
            d1_est = np.linalg.norm(S - M1)
            d2_est = np.linalg.norm(S - M2)
            d3_est = np.linalg.norm(S - M3)
            return (d1_est - d1)**2 + (d2_est - d2)**2 + (d3_est - d3)**2

        # initial guess for the source position (can be the centroid of the triangle for a starting point)
        initial_guess = (M1 + M2 + M3) / 3

        # optimization
        result = minimize(objective_function, initial_guess, method='L-BFGS-B')

        # estimated source position
        S_est = result.x

        # assuming DOA is the angle between the positive x-axis and the line connecting M1 and the source
        doa = np.arctan2(S_est[1], S_est[0]) * (180.0 / np.pi)
        return doa if doa >= 0 else doa + 360


def calculate_doa_coordinates(doa, mic_distance):
    # centroid of the microphone array equilateral triangle
    M1 = np.array([0, 0])
    M2 = np.array([mic_distance, 0])
    M3 = np.array([mic_distance / 2, mic_distance * np.sqrt(3) / 2])
    centroid = (M1 + M2 + M3) / 3

    # degrees to radians
    doa_radians = np.deg2rad(doa)

    # project the DOA from the centroid
    doa_x = centroid[0] + np.cos(doa_radians)
    doa_y = centroid[1] + np.sin(doa_radians)

    return doa_x, doa_y


def triangulation(audioItems: List[AudioItem]):
    moduleDao = DaoFactory.createModuleDao()
    signals = _audioToNpArray(audioItems)
    # calculate TDOA between pairs of microphones
    tau12, _ = gcc_phat(signals[0], signals[1], fs=16000, max_tau=MAX_TDOA)
    tau13, _ = gcc_phat(signals[0], signals[2], fs=16000, max_tau=MAX_TDOA)
    tau23, _ = gcc_phat(signals[1], signals[2], fs=16000, max_tau=MAX_TDOA)
    print(f"Time Delay between Audio 1 and 2: {tau12} seconds")
    print(f"Time Delay between Audio 2 and 3: {tau23} seconds")
    print(f"Time Delay between Audio 1 and 3: {tau13} seconds \n")

    # calculate DOA based on TDOA
    doa = _get_direction([signals[0], signals[1], signals[2]])
    doa_coordinates = calculate_doa_coordinates(doa, MIC_DISTANCE)

    # end_time = time.time()
    # duration = (end_time - start_time) * 1000  # convert to ms
    print(f"Estimated DOA from Mic 1 as Reference Baseline: {doa} degrees")
    print(f"Coordinates of DOA relative to microphone array centroid: {doa_coordinates}\n")
    # print(f"Processing time: {duration:.2f} ms")

    # GETTING COORDINATES OF THE MODULES:
    coordinates = [] # [[x1, y1], [x2, y2], [x3, y3]]
    for item in audioItems:
        module = moduleDao.find_by_id(item.moduleId)
        coordinates.append([module[2], module[3]])
    
    print(coordinates)
