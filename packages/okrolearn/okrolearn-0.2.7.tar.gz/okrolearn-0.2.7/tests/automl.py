from okrolearn.okrolearn import AutoMLFramework, np

automl = AutoMLFramework(temperature=1.0)

# Suggest architecture
input_size = 10
output_size = 1
suggested_architecture, optimizer, scheduler = automl.suggest_architecture(input_size, output_size)

# Apply suggested architecture
automl.apply_suggested_architecture(input_size, output_size)

# Train with suggested architecture
inputs = np.random.rand(100, input_size)
targets = np.random.rand(100, output_size)
losses = automl.train_with_suggested_architecture(inputs, targets, input_size, output_size)

# Rank network performance
test_inputs = np.random.rand(20, input_size)
test_targets = np.random.rand(20, output_size)
performance = automl.rank_network_performance(test_inputs, test_targets, temperature=1.0)
