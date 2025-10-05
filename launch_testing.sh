#!/bin/bash

# 🧪 LAUNCH TESTING INFRASTRUCTURE
# ================================
# 
# Comprehensive launcher for all testing components:
# - Unit tests for business rules
# - Integration tests for file processing
# - Performance tests for large datasets  
# - Regression tests for rule changes
# - Business rule configuration UI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    print_success "Python 3 found"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found, creating..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment found"
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install requirements
install_requirements() {
    print_info "Installing/updating requirements..."
    pip install -q --upgrade pip
    
    # Core requirements
    pip install -q pandas streamlit plotly openpyxl
    
    # Testing requirements
    pip install -q psutil memory-profiler
    
    print_success "Requirements installed"
}

# Check if tests directory exists
check_tests_directory() {
    if [ ! -d "tests" ]; then
        print_error "Tests directory not found!"
        print_info "Please ensure you have the complete testing infrastructure"
        exit 1
    fi
    print_success "Tests directory found"
}

# Run unit tests
run_unit_tests() {
    print_header "🧪 Running Unit Tests for Business Rules"
    python3 run_all_tests.py --unit-only --verbose
    return $?
}

# Run integration tests
run_integration_tests() {
    print_header "🔄 Running Integration Tests for File Processing"
    python3 run_all_tests.py --integration-only --verbose
    return $?
}

# Run performance tests
run_performance_tests() {
    print_header "⚡ Running Performance Tests for Large Datasets"
    python3 run_all_tests.py --performance-only --verbose
    return $?
}

# Run regression tests
run_regression_tests() {
    print_header "🔄 Running Regression Tests for Rule Changes"
    python3 run_all_tests.py --regression-only --verbose
    return $?
}

# Run all tests
run_all_tests() {
    print_header "🚀 Running Comprehensive Test Suite"
    python3 run_all_tests.py --performance --regression --verbose
    return $?
}

# Launch business rule configuration UI
launch_config_ui() {
    print_header "⚙️ Launching Business Rule Configuration UI"
    print_info "Starting Streamlit server..."
    streamlit run business_rule_config_ui.py --server.port 8513 --server.headless true
}

# Main menu
show_menu() {
    echo
    print_header "🧪 TIMESHEET TESTING INFRASTRUCTURE LAUNCHER"
    echo "=============================================="
    echo
    echo "Available options:"
    echo
    echo "  1) 🧪 Run Unit Tests (Business Rules)"
    echo "  2) 🔄 Run Integration Tests (File Processing)"
    echo "  3) ⚡ Run Performance Tests (Large Datasets)"
    echo "  4) 🔄 Run Regression Tests (Rule Changes)"
    echo "  5) 🚀 Run ALL Tests (Comprehensive Suite)"
    echo "  6) ⚙️  Launch Business Rule Configuration UI"
    echo "  7) 📊 System Information"
    echo "  8) 🛠️  Setup/Repair Environment"
    echo "  9) ❌ Exit"
    echo
}

# System information
show_system_info() {
    print_header "📊 System Information"
    echo "Python Version: $(python3 --version)"
    echo "Current Directory: $(pwd)"
    echo "Available Memory: $(free -h | grep '^Mem:' | awk '{print $7}' 2>/dev/null || echo 'N/A')"
    echo "CPU Cores: $(nproc 2>/dev/null || echo 'N/A')"
    echo
    print_info "Checking Python packages..."
    python3 -c "
import sys
packages = ['pandas', 'streamlit', 'plotly', 'openpyxl', 'psutil', 'memory_profiler']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        print(f'❌ {pkg} (missing)')
"
}

# Setup environment
setup_environment() {
    print_header "🛠️  Setting Up Testing Environment"
    check_python
    check_venv
    activate_venv
    install_requirements
    check_tests_directory
    print_success "Environment setup complete!"
}

# Main execution
main() {
    # Initial checks
    check_python
    check_tests_directory
    
    # Show menu and handle user input
    while true; do
        show_menu
        read -p "Select an option (1-9): " choice
        echo
        
        case $choice in
            1)
                run_unit_tests
                ;;
            2)
                run_integration_tests
                ;;
            3)
                run_performance_tests
                ;;
            4)
                run_regression_tests
                ;;
            5)
                run_all_tests
                ;;
            6)
                launch_config_ui
                ;;
            7)
                show_system_info
                ;;
            8)
                setup_environment
                ;;
            9)
                print_success "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please select 1-9."
                ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Handle command line arguments
if [ $# -eq 0 ]; then
    # No arguments, show interactive menu
    main
else
    # Handle command line arguments
    case $1 in
        "unit"|"--unit")
            run_unit_tests
            ;;
        "integration"|"--integration")
            run_integration_tests
            ;;
        "performance"|"--performance")
            run_performance_tests
            ;;
        "regression"|"--regression")
            run_regression_tests
            ;;
        "all"|"--all")
            run_all_tests
            ;;
        "config"|"--config")
            launch_config_ui
            ;;
        "setup"|"--setup")
            setup_environment
            ;;
        "info"|"--info")
            show_system_info
            ;;
        "help"|"--help"|"-h")
            echo "Usage: $0 [option]"
            echo
            echo "Options:"
            echo "  unit         Run unit tests"
            echo "  integration  Run integration tests"
            echo "  performance  Run performance tests"
            echo "  regression   Run regression tests"
            echo "  all          Run all tests"
            echo "  config       Launch configuration UI"
            echo "  setup        Setup environment"
            echo "  info         Show system information"
            echo "  help         Show this help"
            echo
            echo "Run without arguments for interactive menu."
            ;;
        *)
            print_error "Unknown option: $1"
            print_info "Use '$0 help' for available options"
            exit 1
            ;;
    esac
fi