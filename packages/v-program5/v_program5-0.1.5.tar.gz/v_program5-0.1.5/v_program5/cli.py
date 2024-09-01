from v_program5.ml_model import train_model, predict_model

def main():
    print("Running CLI...")
    # Example data to pass to the model
    data = [
        [14.23, 1.71, 2.43, 15.6, 127.0, 2.80, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0],
        [13.20, 1.78, 2.14, 11.2, 100.0, 2.65, 2.76, 0.26, 1.28, 4.38, 1.05, 3.40, 1050.0]
        # Add more rows as needed
    ]
    train_model(data)
    predict_model(data)

if __name__ == "__main__":
    main()
