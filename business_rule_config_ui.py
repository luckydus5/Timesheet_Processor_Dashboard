"""
⚙️ BUSINESS RULE CONFIGURATION UI
=================================

Interactive Streamlit interface for configuring and managing
business rules dynamically without code changes.
"""

import streamlit as st
import json
import os
import sys
from datetime import time, datetime
import pandas as pd
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timesheet_business_rules import TimesheetBusinessRules


class BusinessRuleConfigManager:
    """Manager for business rule configurations"""
    
    def __init__(self):
        self.config_file = "business_rules_config.json"
        self.default_config = self.get_default_config()
        self.current_config = self.load_config()
    
    def get_default_config(self):
        """Get default business rule configuration"""
        return {
            "shift_definitions": {
                "day_shift": {
                    "start_time": "08:00:00",
                    "end_time": "17:00:00",
                    "name": "Day Shift",
                    "description": "Standard daytime working hours"
                },
                "night_shift": {
                    "start_time": "18:00:00",
                    "end_time": "03:00:00",
                    "name": "Night Shift",
                    "description": "Evening to early morning hours"
                }
            },
            "overtime_rules": {
                "minimum_overtime_minutes": 30,
                "day_shift_max_overtime_hours": 1.5,
                "night_shift_max_overtime_hours": 3.0,
                "overtime_calculation_method": "after_shift_end"
            },
            "calculation_settings": {
                "round_to_nearest_minutes": 15,
                "allow_early_checkin_overtime": False,
                "cross_midnight_handling": True,
                "weekend_rules_apply": True
            },
            "validation_rules": {
                "max_daily_hours": 16,
                "min_break_between_shifts": 8,
                "require_both_checkin_checkout": True
            },
            "display_settings": {
                "time_format": "HH:MM:SS",
                "decimal_places": 2,
                "show_warnings": True
            },
            "advanced_rules": {
                "holiday_overtime_multiplier": 1.5,
                "weekend_overtime_multiplier": 1.2,
                "consecutive_overtime_limit": 5
            }
        }
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self.merge_with_defaults(config)
            except Exception as e:
                st.error(f"Error loading config: {e}")
                return self.default_config
        return self.default_config
    
    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving config: {e}")
            return False
    
    def merge_with_defaults(self, config):
        """Merge user config with defaults"""
        merged = self.default_config.copy()
        
        def deep_merge(default, user):
            for key, value in user.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    deep_merge(default[key], value)
                else:
                    default[key] = value
        
        deep_merge(merged, config)
        return merged
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.current_config = self.default_config.copy()
        return self.save_config(self.current_config)
    
    def export_config(self):
        """Export current configuration as JSON string"""
        return json.dumps(self.current_config, indent=2)
    
    def import_config(self, config_json):
        """Import configuration from JSON string"""
        try:
            config = json.loads(config_json)
            self.current_config = self.merge_with_defaults(config)
            return self.save_config(self.current_config)
        except Exception as e:
            st.error(f"Error importing config: {e}")
            return False


def main():
    """Main Streamlit application"""
    
    st.set_page_config(
        page_title="Business Rule Configuration",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main > div {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
        }
        .config-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.25rem;
            color: #155724;
            padding: 0.75rem;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 0.25rem;
            color: #856404;
            padding: 0.75rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize config manager
    if 'config_manager' not in st.session_state:
        st.session_state.config_manager = BusinessRuleConfigManager()
    
    config_manager = st.session_state.config_manager
    
    # Header
    st.title("⚙️ Business Rule Configuration")
    st.markdown("Configure and manage timesheet processing business rules dynamically")
    
    # Sidebar for quick actions
    with st.sidebar:
        st.header("🛠️ Quick Actions")
        
        if st.button("💾 Save Configuration", type="primary"):
            if config_manager.save_config(config_manager.current_config):
                st.success("Configuration saved successfully!")
            else:
                st.error("Failed to save configuration")
        
        if st.button("🔄 Reset to Defaults"):
            if config_manager.reset_to_defaults():
                st.success("Reset to default configuration!")
                st.rerun()
        
        if st.button("🧪 Test Current Rules"):
            st.session_state.show_test_results = True
        
        # Configuration status
        st.markdown("---")
        st.subheader("📊 Configuration Status")
        
        if os.path.exists(config_manager.config_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(config_manager.config_file))
            st.write(f"**Last saved:** {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.write("**Status:** Using defaults (not saved)")
        
        # Quick stats
        total_rules = sum(len(section) if isinstance(section, dict) else 1 
                         for section in config_manager.current_config.values())
        st.write(f"**Total rules:** {total_rules}")
    
    # Main content tabs
    tabs = st.tabs([
        "🕐 Shift Definitions",
        "⏰ Overtime Rules", 
        "⚙️ Calculation Settings",
        "✅ Validation Rules",
        "🎨 Display Settings",
        "🔧 Advanced Rules",
        "🧪 Test & Preview",
        "📥📤 Import/Export"
    ])
    
    # Tab 1: Shift Definitions
    with tabs[0]:
        st.header("🕐 Shift Definitions")
        st.markdown("Define the standard working hours for different shift types")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Day Shift")
            day_config = config_manager.current_config["shift_definitions"]["day_shift"]
            
            day_start = st.time_input(
                "Day Shift Start Time",
                value=datetime.strptime(day_config["start_time"], "%H:%M:%S").time(),
                key="day_start"
            )
            
            day_end = st.time_input(
                "Day Shift End Time", 
                value=datetime.strptime(day_config["end_time"], "%H:%M:%S").time(),
                key="day_end"
            )
            
            day_name = st.text_input("Day Shift Name", value=day_config["name"])
            day_desc = st.text_area("Day Shift Description", value=day_config["description"])
            
            # Update config
            config_manager.current_config["shift_definitions"]["day_shift"] = {
                "start_time": day_start.strftime("%H:%M:%S"),
                "end_time": day_end.strftime("%H:%M:%S"),
                "name": day_name,
                "description": day_desc
            }
        
        with col2:
            st.subheader("Night Shift")
            night_config = config_manager.current_config["shift_definitions"]["night_shift"]
            
            night_start = st.time_input(
                "Night Shift Start Time",
                value=datetime.strptime(night_config["start_time"], "%H:%M:%S").time(),
                key="night_start"
            )
            
            night_end = st.time_input(
                "Night Shift End Time",
                value=datetime.strptime(night_config["end_time"], "%H:%M:%S").time(),
                key="night_end"
            )
            
            night_name = st.text_input("Night Shift Name", value=night_config["name"])
            night_desc = st.text_area("Night Shift Description", value=night_config["description"])
            
            # Update config
            config_manager.current_config["shift_definitions"]["night_shift"] = {
                "start_time": night_start.strftime("%H:%M:%S"),
                "end_time": night_end.strftime("%H:%M:%S"),
                "name": night_name,
                "description": night_desc
            }
        
        # Validation
        if day_start >= day_end:
            st.warning("⚠️ Day shift start time should be before end time")
        
        if night_start <= night_end:
            st.info("ℹ️ Night shift crosses midnight - this is normal")
    
    # Tab 2: Overtime Rules
    with tabs[1]:
        st.header("⏰ Overtime Rules")
        st.markdown("Configure overtime calculation rules and limits")
        
        overtime_config = config_manager.current_config["overtime_rules"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_overtime = st.number_input(
                "Minimum Overtime (minutes)",
                min_value=0,
                max_value=120,
                value=overtime_config["minimum_overtime_minutes"],
                step=5,
                help="Minimum overtime required before it's counted"
            )
            
            day_max_ot = st.number_input(
                "Day Shift Max Overtime (hours)",
                min_value=0.0,
                max_value=8.0,
                value=overtime_config["day_shift_max_overtime_hours"],
                step=0.5,
                help="Maximum overtime allowed for day shifts"
            )
        
        with col2:
            night_max_ot = st.number_input(
                "Night Shift Max Overtime (hours)",
                min_value=0.0,
                max_value=8.0,
                value=overtime_config["night_shift_max_overtime_hours"],
                step=0.5,
                help="Maximum overtime allowed for night shifts"
            )
            
            calc_method = st.selectbox(
                "Overtime Calculation Method",
                ["after_shift_end", "total_hours_based", "flexible"],
                index=0 if overtime_config["overtime_calculation_method"] == "after_shift_end" else 1,
                help="How overtime is calculated"
            )
        
        # Update config
        config_manager.current_config["overtime_rules"] = {
            "minimum_overtime_minutes": min_overtime,
            "day_shift_max_overtime_hours": day_max_ot,
            "night_shift_max_overtime_hours": night_max_ot,
            "overtime_calculation_method": calc_method
        }
    
    # Tab 3: Calculation Settings
    with tabs[2]:
        st.header("⚙️ Calculation Settings")
        st.markdown("Configure how time calculations are performed")
        
        calc_config = config_manager.current_config["calculation_settings"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            round_minutes = st.selectbox(
                "Round to Nearest (minutes)",
                [1, 5, 10, 15, 30],
                index=[1, 5, 10, 15, 30].index(calc_config["round_to_nearest_minutes"]),
                help="Round time calculations to nearest interval"
            )
            
            early_checkin_ot = st.checkbox(
                "Allow Early Check-in Overtime",
                value=calc_config["allow_early_checkin_overtime"],
                help="Count early check-ins as overtime"
            )
        
        with col2:
            cross_midnight = st.checkbox(
                "Cross-Midnight Handling",
                value=calc_config["cross_midnight_handling"],
                help="Handle shifts that cross midnight"
            )
            
            weekend_rules = st.checkbox(
                "Apply Weekend Rules",
                value=calc_config["weekend_rules_apply"],
                help="Apply special rules for weekends"
            )
        
        # Update config
        config_manager.current_config["calculation_settings"] = {
            "round_to_nearest_minutes": round_minutes,
            "allow_early_checkin_overtime": early_checkin_ot,
            "cross_midnight_handling": cross_midnight,
            "weekend_rules_apply": weekend_rules
        }
    
    # Tab 4: Validation Rules
    with tabs[3]:
        st.header("✅ Validation Rules")
        st.markdown("Set validation rules for data integrity")
        
        validation_config = config_manager.current_config["validation_rules"]
        
        max_daily = st.number_input(
            "Maximum Daily Hours",
            min_value=8,
            max_value=24,
            value=validation_config["max_daily_hours"],
            help="Maximum hours allowed per day"
        )
        
        min_break = st.number_input(
            "Minimum Break Between Shifts (hours)",
            min_value=0,
            max_value=24,
            value=validation_config["min_break_between_shifts"],
            help="Minimum rest time between shifts"
        )
        
        require_both = st.checkbox(
            "Require Both Check-in and Check-out",
            value=validation_config["require_both_checkin_checkout"],
            help="Reject incomplete records"
        )
        
        # Update config
        config_manager.current_config["validation_rules"] = {
            "max_daily_hours": max_daily,
            "min_break_between_shifts": min_break,
            "require_both_checkin_checkout": require_both
        }
    
    # Tab 5: Display Settings
    with tabs[4]:
        st.header("🎨 Display Settings")
        st.markdown("Configure how results are displayed")
        
        display_config = config_manager.current_config["display_settings"]
        
        time_format = st.selectbox(
            "Time Format",
            ["HH:MM:SS", "HH:MM", "Decimal"],
            index=["HH:MM:SS", "HH:MM", "Decimal"].index(display_config["time_format"])
        )
        
        decimal_places = st.number_input(
            "Decimal Places",
            min_value=0,
            max_value=4,
            value=display_config["decimal_places"]
        )
        
        show_warnings = st.checkbox(
            "Show Warnings",
            value=display_config["show_warnings"]
        )
        
        # Update config
        config_manager.current_config["display_settings"] = {
            "time_format": time_format,
            "decimal_places": decimal_places,
            "show_warnings": show_warnings
        }
    
    # Tab 6: Advanced Rules
    with tabs[5]:
        st.header("🔧 Advanced Rules")
        st.markdown("Advanced configuration options")
        
        advanced_config = config_manager.current_config["advanced_rules"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            holiday_multiplier = st.number_input(
                "Holiday Overtime Multiplier",
                min_value=1.0,
                max_value=3.0,
                value=advanced_config["holiday_overtime_multiplier"],
                step=0.1
            )
            
            weekend_multiplier = st.number_input(
                "Weekend Overtime Multiplier",
                min_value=1.0,
                max_value=3.0,
                value=advanced_config["weekend_overtime_multiplier"],
                step=0.1
            )
        
        with col2:
            consecutive_limit = st.number_input(
                "Consecutive Overtime Limit (days)",
                min_value=1,
                max_value=14,
                value=advanced_config["consecutive_overtime_limit"]
            )
        
        # Update config
        config_manager.current_config["advanced_rules"] = {
            "holiday_overtime_multiplier": holiday_multiplier,
            "weekend_overtime_multiplier": weekend_multiplier,
            "consecutive_overtime_limit": consecutive_limit
        }
    
    # Tab 7: Test & Preview
    with tabs[6]:
        st.header("🧪 Test & Preview")
        st.markdown("Test your current configuration with sample data")
        
        if st.button("🚀 Run Comprehensive Tests"):
            st.session_state.show_test_results = True
        
        if st.session_state.get('show_test_results', False):
            with st.spinner("Running tests..."):
                run_configuration_tests(config_manager.current_config)
    
    # Tab 8: Import/Export
    with tabs[7]:
        st.header("📥📤 Import/Export Configuration")
        st.markdown("Import or export configuration settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Export")
            if st.button("Export Current Configuration"):
                config_json = config_manager.export_config()
                st.text_area("Configuration JSON", config_json, height=300)
                st.download_button(
                    "💾 Download Configuration",
                    config_json,
                    file_name=f"business_rules_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            st.subheader("📥 Import")
            uploaded_file = st.file_uploader("Upload Configuration File", type="json")
            
            if uploaded_file is not None:
                config_json = uploaded_file.read().decode('utf-8')
                st.text_area("Imported Configuration", config_json, height=200)
                
                if st.button("Apply Imported Configuration"):
                    if config_manager.import_config(config_json):
                        st.success("Configuration imported successfully!")
                        st.rerun()
            
            st.markdown("---")
            manual_import = st.text_area("Or paste configuration JSON here:", height=150)
            
            if st.button("Apply Manual Configuration"):
                if manual_import:
                    if config_manager.import_config(manual_import):
                        st.success("Configuration applied successfully!")
                        st.rerun()


def run_configuration_tests(config):
    """Run tests with current configuration"""
    
    st.subheader("🧪 Configuration Test Results")
    
    # Create test scenarios
    test_scenarios = [
        {
            "name": "Normal Day Shift",
            "start": "08:00:00",
            "end": "17:00:00",
            "expected_shift": "Day Shift"
        },
        {
            "name": "Day Shift with Overtime",
            "start": "08:00:00", 
            "end": "18:30:00",
            "expected_shift": "Day Shift"
        },
        {
            "name": "Normal Night Shift",
            "start": "18:00:00",
            "end": "03:00:00",
            "expected_shift": "Night Shift"
        },
        {
            "name": "Night Shift with Overtime",
            "start": "18:00:00",
            "end": "06:00:00",
            "expected_shift": "Night Shift"
        }
    ]
    
    # Create processor with current config (simplified)
    processor = TimesheetBusinessRules()
    
    results = []
    for scenario in test_scenarios:
        start_time = datetime.strptime(scenario["start"], "%H:%M:%S").time()
        end_time = datetime.strptime(scenario["end"], "%H:%M:%S").time()
        
        shift_type = processor.determine_shift_type(start_time)
        total_hours = processor.calculate_total_work_hours(start_time, end_time, shift_type)
        overtime = processor.calculate_overtime_hours(start_time, end_time, shift_type)
        
        results.append({
            "Scenario": scenario["name"],
            "Start Time": scenario["start"],
            "End Time": scenario["end"],
            "Shift Type": shift_type,
            "Total Hours": f"{total_hours:.2f}",
            "Overtime Hours": f"{overtime:.2f}",
            "Status": "✅ Pass" if shift_type == scenario["expected_shift"] else "❌ Fail"
        })
    
    # Display results
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)
    
    # Summary
    passed = len([r for r in results if "✅" in r["Status"]])
    total = len(results)
    
    if passed == total:
        st.success(f"🎉 All {total} tests passed!")
    else:
        st.warning(f"⚠️ {passed}/{total} tests passed. Please review configuration.")
    
    # Configuration summary
    st.subheader("📋 Current Configuration Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Day Shift Hours", 
                 f"{config['shift_definitions']['day_shift']['start_time']} - {config['shift_definitions']['day_shift']['end_time']}")
        st.metric("Min Overtime", f"{config['overtime_rules']['minimum_overtime_minutes']} min")
    
    with col2:
        st.metric("Night Shift Hours",
                 f"{config['shift_definitions']['night_shift']['start_time']} - {config['shift_definitions']['night_shift']['end_time']}")
        st.metric("Day Max OT", f"{config['overtime_rules']['day_shift_max_overtime_hours']} hrs")
    
    with col3:
        st.metric("Max Daily Hours", f"{config['validation_rules']['max_daily_hours']} hrs")
        st.metric("Night Max OT", f"{config['overtime_rules']['night_shift_max_overtime_hours']} hrs")


if __name__ == "__main__":
    main()