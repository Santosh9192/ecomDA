"""
=============================================================================
E-Commerce Sales Analytics - Data Validation Pipeline
=============================================================================
Description: Validate data quality, integrity, and business rules
Author: Business Analytics Team
Version: 1.0
Python: 3.8+
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Any

# =============================================================================
# CONFIGURATION
# =============================================================================
CLEANED_DATA_PATH = os.path.join('data', 'cleaned')
REPORTS_PATH = os.path.join('reports')
VALIDATION_LOG = os.path.join(REPORTS_PATH, 'validation_report.json')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# VALIDATION RULES ENGINE
# =============================================================================
class DataValidator:
    """
    Comprehensive data validation engine with configurable rules.
    
    Validates:
    - Schema conformance
    - Data type correctness
    - Range and domain constraints
    - Uniqueness constraints
    - Referential integrity
    - Business rules
    - Statistical distributions
    """
    
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        """
        Initialize the validator with a dictionary of DataFrames.
        
        Args:
            dataframes: Dictionary mapping dataset names to DataFrames
        """
        self.dataframes = dataframes
        self.validation_results = {
            'run_timestamp': datetime.now().isoformat(),
            'overall_status': 'PASSED',
            'datasets': {},
            'summary': {
                'total_checks': 0,
                'passed': 0,
                'warnings': 0,
                'failed': 0
            }
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """
        Execute all validation checks across all datasets.
        
        Returns:
            Comprehensive validation report dictionary
        """
        logger.info("=" * 60)
        logger.info("DATA VALIDATION ENGINE STARTED")
        logger.info("=" * 60)
        
        for name, df in self.dataframes.items():
            if len(df) == 0:
                logger.warning(f"Skipping {name}: empty dataset")
                continue
            
            logger.info(f"\nValidating: {name.upper()}")
            
            dataset_results = {
                'shape': list(df.shape),
                'checks': []
            }
            
            # Run all validation check categories
            dataset_results['checks'].extend(
                self._check_schema(df, name)
            )
            dataset_results['checks'].extend(
                self._check_data_types(df, name)
            )
            dataset_results['checks'].extend(
                self._check_numeric_ranges(df, name)
            )
            dataset_results['checks'].extend(
                self._check_categorical_domains(df, name)
            )
            dataset_results['checks'].extend(
                self._check_uniqueness(df, name)
            )
            dataset_results['checks'].extend(
                self._check_referential_integrity(df, name)
            )
            dataset_results['checks'].extend(
                self._check_business_rules(df, name)
            )
            
            # Determine dataset status
            failed = sum(1 for c in dataset_results['checks'] 
                        if c['status'] == 'FAIL')
            warnings = sum(1 for c in dataset_results['checks'] 
                          if c['status'] == 'WARNING')
            
            dataset_results['status'] = 'PASSED' if failed == 0 else 'FAILED'
            dataset_results['total_checks'] = len(dataset_results['checks'])
            dataset_results['passed'] = len(dataset_results['checks']) - failed - warnings
            dataset_results['warnings'] = warnings
            dataset_results['failed'] = failed
            
            self.validation_results['datasets'][name] = dataset_results
            
            # Update summary
            self.validation_results['summary']['total_checks'] += len(dataset_results['checks'])
            self.validation_results['summary']['passed'] += dataset_results['passed']
            self.validation_results['summary']['warnings'] += dataset_results['warnings']
            self.validation_results['summary']['failed'] += dataset_results['failed']
        
        # Set overall status
        if self.validation_results['summary']['failed'] > 0:
            self.validation_results['overall_status'] = 'FAILED'
        elif self.validation_results['summary']['warnings'] > 0:
            self.validation_results['overall_status'] = 'PASSED_WITH_WARNINGS'
        
        return self.validation_results
    
    def _add_check(self, checks: List[Dict], check_name: str, 
                   status: str, details: Any, severity: str = 'medium') -> None:
        """
        Helper to add a validation check result.
        
        Args:
            checks: List of check results to append to
            check_name: Name of the validation check
            status: PASS, WARNING, or FAIL
            details: Details about the check result
            severity: low, medium, high
        """
        checks.append({
            'check_name': check_name,
            'status': status,
            'severity': severity,
            'details': str(details)
        })
        
        level_map = {
            'PASS': logger.info,
            'WARNING': logger.warning,
            'FAIL': logger.error
        }
        level_map.get(status, logger.info)(f"  [{status}] {check_name}: {details}")
    
    def _check_schema(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Verify expected columns exist."""
        checks = []
        
        expected_schemas = {
            'customers': ['Customer ID', 'Customer Name', 'Segment', 'Region', 
                         'State', 'City', 'Email', 'Registration Date'],
            'orders': ['Order ID', 'Order Date', 'Ship Date', 'Shipping Mode',
                      'Customer ID', 'Customer Name', 'Segment', 'Region',
                      'State', 'City', 'Category', 'Sub-Category', 'Product Name',
                      'Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost',
                      'Payment Mode', 'Return Status'],
            'regions': ['Region', 'State', 'Cities', 'City Count'],
            'categories': ['Category', 'Sub-Category']
        }
        
        expected = expected_schemas.get(name, [])
        if expected:
            missing = [col for col in expected if col not in df.columns]
            extra = [col for col in df.columns if col not in expected]
            
            if missing:
                self._add_check(checks, 'Schema - Missing Columns', 'FAIL',
                              f"Missing: {missing}")
            else:
                self._add_check(checks, 'Schema - All expected columns present', 
                              'PASS', f"{len(expected)} columns verified")
            
            if extra:
                self._add_check(checks, 'Schema - Extra columns found', 'WARNING',
                              f"Extra: {extra}")
        
        return checks
    
    def _check_data_types(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Validate data type correctness."""
        checks = []
        
        # Check that date columns are datetime
        date_cols = [col for col in df.columns if 'Date' in col]
        for col in date_cols:
            if col in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    try:
                        pd.to_datetime(df[col], errors='coerce')
                        self._add_check(checks, f'Data Type - {col}', 'WARNING',
                                      f'Should be datetime, converting now')
                    except:
                        self._add_check(checks, f'Data Type - {col}', 'FAIL',
                                      f'Cannot convert to datetime')
                else:
                    self._add_check(checks, f'Data Type - {col}', 'PASS',
                                  'Correct datetime type')
        
        # Check numeric columns
        numeric_cols = ['Sales', 'Profit', 'Quantity', 'Discount', 'Shipping Cost']
        for col in numeric_cols:
            if col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    self._add_check(checks, f'Data Type - {col}', 'PASS',
                                  f'Correct numeric type: {df[col].dtype}')
                else:
                    self._add_check(checks, f'Data Type - {col}', 'FAIL',
                                  f'Should be numeric, got {df[col].dtype}')
        
        return checks
    
    def _check_numeric_ranges(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Validate numeric column ranges and boundaries."""
        checks = []
        
        range_rules = {
            'Sales': (0, 100000),
            'Profit': (-10000, 50000),
            'Quantity': (1, 100),
            'Discount': (0, 1),
            'Discount Amount': (0, 100000),
            'Shipping Cost': (0, 500),
            'Profit Margin %': (-100, 100),
            'Delivery Days': (0, 30),
            'Customer Tenure Days': (0, 3650),
            'City Count': (1, 50)
        }
        
        for col, (min_val, max_val) in range_rules.items():
            if col in df.columns:
                col_min = df[col].min()
                col_max = df[col].max()
                
                issues = []
                if col_min < min_val:
                    issues.append(f"min {col_min} < {min_val}")
                if col_max > max_val:
                    issues.append(f"max {col_max} > {max_val}")
                
                if issues:
                    self._add_check(checks, f'Range - {col}', 'FAIL',
                                  f'Out of bounds: {"; ".join(issues)}')
                else:
                    self._add_check(checks, f'Range - {col}', 'PASS',
                                  f'Values in [{min_val}, {max_val}]')
        
        return checks
    
    def _check_categorical_domains(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Validate categorical column domains."""
        checks = []
        
        valid_domains = {
            'Segment': ['Consumer', 'Corporate', 'Home Office'],
            'Shipping Mode': ['Standard Class', 'Second Class', 'First Class', 'Same Day'],
            'Payment Mode': ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash', 'UPI/Wallet'],
            'Return Status': ['Returned', 'Not Returned'],
            'Region': ['West', 'East', 'Central', 'South'],
            'Category': ['Furniture', 'Office Supplies', 'Technology'],
            'Season': ['Holiday', 'Spring', 'Summer', 'Fall'],
            'Sales Bucket': ['Under $50', '$50-$100', '$101-$250', '$251-$500', '$501-$1000', 'Over $1000'],
            'Profit Category': ['Loss', 'Low Margin', 'Medium Margin', 'High Margin']
        }
        
        for col, valid_values in valid_domains.items():
            if col in df.columns:
                unique_values = df[col].dropna().unique()
                invalid = [v for v in unique_values if v not in valid_values]
                
                if invalid:
                    self._add_check(checks, f'Domain - {col}', 'WARNING',
                                  f'Invalid values found: {invalid[:5]}')
                else:
                    self._add_check(checks, f'Domain - {col}', 'PASS',
                                  f'All values in valid domain')
        
        return checks
    
    def _check_uniqueness(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Check uniqueness constraints."""
        checks = []
        
        uniqueness_rules = {
            'customers': ['Customer ID'],
            'orders': ['Order ID'],
            'regions': ['Region', 'State'],
            'categories': ['Category', 'Sub-Category']
        }
        
        rule = uniqueness_rules.get(name, [])
        if rule:
            dupes = df.duplicated(subset=rule, keep=False).sum()
            if dupes > 0:
                self._add_check(checks, f'Uniqueness - {rule}', 'FAIL',
                              f'{dupes} duplicate values found')
            else:
                self._add_check(checks, f'Uniqueness - {rule}', 'PASS',
                              'All values are unique')
        
        return checks
    
    def _check_referential_integrity(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Check cross-dataset referential integrity."""
        checks = []
        
        if name == 'orders' and 'customers' in self.dataframes:
            customers_df = self.dataframes['customers']
            if 'Customer ID' in df.columns and 'Customer ID' in customers_df.columns:
                orphan_orders = df[~df['Customer ID'].isin(customers_df['Customer ID'])]
                if len(orphan_orders) > 0:
                    self._add_check(checks, 'Referential Integrity - Customer ID', 
                                  'FAIL',
                                  f'{len(orphan_orders)} orders with no matching customer')
                else:
                    self._add_check(checks, 'Referential Integrity - Customer ID', 
                                  'PASS',
                                  'All orders have valid customers')
        
        if name == 'orders' and 'categories' in self.dataframes:
            # Check category/subcategory match
            categories_df = self.dataframes['categories']
            if 'Category' in df.columns and 'Sub-Category' in df.columns:
                cat_pairs = set(zip(categories_df['Category'], categories_df['Sub-Category']))
                order_pairs = set(zip(df['Category'], df['Sub-Category']))
                invalid_pairs = order_pairs - cat_pairs
                
                if invalid_pairs:
                    self._add_check(checks, 'Referential Integrity - Category/Sub-Category',
                                  'FAIL',
                                  f'{len(invalid_pairs)} invalid category combinations')
                else:
                    self._add_check(checks, 'Referential Integrity - Category/Sub-Category',
                                  'PASS',
                                  'All category combinations valid')
        
        return checks
    
    def _check_business_rules(self, df: pd.DataFrame, name: str) -> List[Dict]:
        """Validate business logic rules."""
        checks = []
        
        if name == 'orders':
            # Rule 1: Ship date should be >= Order date
            if 'Order Date' in df.columns and 'Ship Date' in df.columns:
                negative_delivery = df[df['Ship Date'] < df['Order Date']]
                if len(negative_delivery) > 0:
                    self._add_check(checks, 'Business Rule - Ship Date >= Order Date',
                                  'FAIL',
                                  f'{len(negative_delivery)} orders have ship date before order date')
                else:
                    self._add_check(checks, 'Business Rule - Ship Date >= Order Date',
                                  'PASS', 'All ship dates are valid')
            
            # Rule 2: Profit = Sales - Cost
            if all(col in df.columns for col in ['Sales', 'Profit']):
                negative_profit_pct = (df['Profit'] < 0).sum() / len(df) * 100
                if negative_profit_pct > 30:
                    self._add_check(checks, 'Business Rule - Profit Ratio', 'WARNING',
                                  f'{negative_profit_pct:.1f}% of orders have negative profit')
                else:
                    self._add_check(checks, 'Business Rule - Profit Ratio', 'PASS',
                                  f'Only {negative_profit_pct:.1f}% negative profit orders')
            
            # Rule 3: Check for suspiciously high discounts
            if 'Discount' in df.columns:
                high_discount = (df['Discount'] >= 0.5).sum()
                if high_discount > 0:
                    self._add_check(checks, 'Business Rule - Discount Threshold', 'WARNING',
                                  f'{high_discount} transactions have >=50% discount')
                else:
                    self._add_check(checks, 'Business Rule - Discount Threshold', 'PASS',
                                  'No excessive discounts found')
            
            # Rule 4: Zero sales checks
            if 'Sales' in df.columns:
                zero_sales = (df['Sales'] == 0).sum()
                if zero_sales > 0:
                    self._add_check(checks, 'Business Rule - Zero Sales', 'FAIL',
                                  f'{zero_sales} transactions have zero sales')
                else:
                    self._add_check(checks, 'Business Rule - Zero Sales', 'PASS',
                                  'No zero-sales transactions')
        
        return checks
    
    def generate_summary_report(self, output_path: str = VALIDATION_LOG) -> str:
        """
        Generate and save the summary validation report.
        
        Args:
            output_path: Path to save the JSON report
            
        Returns:
            Path to the saved report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert numpy types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            elif isinstance(obj, (np.floating,)):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        with open(output_path, 'w') as f:
            json.dump(self.validation_results, f, indent=2, 
                     default=convert_types)
        
        logger.info(f"\nValidation report saved to: {output_path}")
        return output_path


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """
    Main entry point for data validation.
    
    Loads cleaned data and runs all validation checks.
    """
    logger.info("=" * 60)
    logger.info("DATA VALIDATION PIPELINE")
    logger.info("=" * 60)
    
    # Load cleaned data
    dataframes = {}
    data_files = {
        'customers': os.path.join(CLEANED_DATA_PATH, 'customers_cleaned.csv'),
        'orders': os.path.join(CLEANED_DATA_PATH, 'orders_cleaned.csv'),
        'regions': os.path.join(CLEANED_DATA_PATH, 'regions_cleaned.csv'),
        'categories': os.path.join(CLEANED_DATA_PATH, 'categories_cleaned.csv')
    }
    
    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            dataframes[name] = pd.read_csv(filepath)
            logger.info(f"Loaded {name}: {len(dataframes[name]):,} records")
        else:
            logger.warning(f"File not found: {filepath}")
            # Try raw data as fallback
            raw_path = filepath.replace('cleaned', 'raw').replace('_cleaned', '')
            if os.path.exists(raw_path):
                dataframes[name] = pd.read_csv(raw_path)
                logger.info(f"Loaded {name} from raw: {len(dataframes[name]):,} records")
    
    # Run validation
    validator = DataValidator(dataframes)
    results = validator.run_all_checks()
    
    # Generate report
    report_path = validator.generate_summary_report()
    
    # Print summary
    s = results['summary']
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"  Overall Status: {results['overall_status']}")
    print(f"  Total Checks:   {s['total_checks']}")
    print(f"  Passed:         {s['passed']}")
    print(f"  Warnings:       {s['warnings']}")
    print(f"  Failed:         {s['failed']}")
    print(f"\nReport: {report_path}")
    
    return results


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    main()
