import stim


def make_circuit(distance: int, p: float = 0.0, rounds: int | None = None) -> stim.Circuit:
    """Surface-code memory circuit in Z basis.

    p is the physical error probability of a uniform circuit-level depolarizing
    noise model.
    """
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds if rounds is not None else distance,
        after_clifford_depolarization=p,
        before_round_data_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
    )


if __name__ == "__main__":
    circuit = make_circuit(distance=3)
    print("qubits:", len(circuit.get_final_qubit_coordinates()))
    print("detectors:", circuit.num_detectors)
    print("observables:", circuit.num_observables)

    # check no flips
    detections, flips = circuit.compile_detector_sampler().sample(10_000, separate_observables=True)
    print("noiseless check:", not detections.any() and not flips.any())

    # check for non-zero flips and detections with noise
    noisy = make_circuit(distance=3, p=1e-3)
    detections, flips = noisy.compile_detector_sampler().sample(10_000, separate_observables=True)
    print("noisy check:", detections.any() and flips.any())
