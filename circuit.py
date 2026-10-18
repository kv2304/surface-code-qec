import stim


def make_circuit(distance: int, rounds: int | None = None) -> stim.Circuit:
    """surface-code memory circuit in Z basis."""
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds if rounds is not None else distance,
    )


if __name__ == "__main__":
    circuit = make_circuit(distance=3)
    print("qubits:", len(circuit.get_final_qubit_coordinates()))
    print("detectors:", circuit.num_detectors)
    print("observables:", circuit.num_observables)

    # check no flips
    detections, flips = circuit.compile_detector_sampler().sample(10_000, separate_observables=True)
    print("noiseless check:", not detections.any() and not flips.any())
