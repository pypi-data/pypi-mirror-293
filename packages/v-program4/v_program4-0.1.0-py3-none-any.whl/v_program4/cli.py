import argparse
from v_program4 import train_network, predict, initialize_network

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Neural Network CLI")
    parser.add_argument('--train', action='store_true', help="Train the neural network")
    parser.add_argument('--predict', nargs='+', type=float, help="Make a prediction with the neural network")

    args = parser.parse_args()

    # Example dataset for training
    dataset = [
        [2.7810836, 2.550537003, 0],
        [1.465489372, 2.362125076, 0],
        [3.396561688, 4.400293529, 0],
        [1.38807019, 1.850220317, 0],
        [3.06407232, 3.005305973, 0],
        [7.627531214, 2.759262235, 1],
        [5.332441248, 2.088626775, 1],
        [6.922596716, 1.77106367, 1],
        [8.675418651, -0.242068655, 1],
        [7.673756466, 3.508563011, 1],
    ]

    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set(row[-1] for row in dataset))

    if args.train:
        network = initialize_network(n_inputs, 2, n_outputs)
        train_network(network, dataset, 0.5, 20, n_outputs)
        print("Training complete.")
    elif args.predict:
        if len(args.predict) != n_inputs:
            print(f"Please provide exactly {n_inputs} input values.")
            return
        network = initialize_network(n_inputs, 2, n_outputs)
        # Assuming the network is already trained
        # If the network needs to be saved and loaded, handle that here.
        prediction = predict(network, args.predict + [0])  # Adding dummy label for prediction
        print(f"Prediction: {prediction}")
    else:
        print("No action specified. Use --train to train the network or --predict to make a prediction.")

if __name__ == "__main__":
    main()
