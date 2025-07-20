#!/bin/bash

# setup.sh
echo "Setting up Automation..."

if command -v python3 &>/dev/null; then
    echo "Found Python 3: $(python3 --version)"
else
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Making scripts executable..."
chmod +x posting/post.py
chmod +x posting/setup_env_variables.py

echo "Creating launchers..."
cat > run_post.sh << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 posting/post.py
EOL
chmod +x run_post.sh

cat > setup_env.sh << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 posting/setup_env_variables.py
EOL
chmod +x setup_env.sh

echo "Setup complete! You can now run the applications by:"
echo "1. Double-clicking run_post.sh to post"
echo "2. Double-clicking setup_env.sh to set up environment variables"
echo "3. Or running: ./posting/post.py or ./posting/setup_env_variables.py"