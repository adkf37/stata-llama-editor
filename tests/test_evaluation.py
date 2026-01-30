"""
Stata Editor Evaluation Suite
Tests the AI's performance on Stata-specific tasks
"""

import sys
from pathlib import Path
import time
import json
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llama_client import LlamaClient
from stata_helper import StataHelper


class StataEvaluator:
    """Evaluates the Stata editor's performance on various tasks"""
    
    def __init__(self):
        self.client = LlamaClient()
        self.helper = StataHelper()
        self.results = []
        
    def evaluate_all(self) -> Dict[str, Any]:
        """Run all evaluation tests"""
        print("🧪 Starting Stata Editor Evaluation Suite\n")
        print("=" * 70)
        
        categories = [
            ("Basic Commands", self.test_basic_commands),
            ("Code Explanation", self.test_code_explanation),
            ("Debugging", self.test_debugging),
            ("Optimization", self.test_optimization),
            ("Best Practices", self.test_best_practices),
            ("Edge Cases", self.test_edge_cases),
        ]
        
        overall_results = {
            'categories': {},
            'total_tests': 0,
            'total_passed': 0,
            'avg_response_time': 0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        total_time = 0
        
        for category_name, test_func in categories:
            print(f"\n📋 Testing: {category_name}")
            print("-" * 70)
            
            category_results = test_func()
            overall_results['categories'][category_name] = category_results
            overall_results['total_tests'] += category_results['total']
            overall_results['total_passed'] += category_results['passed']
            total_time += category_results['total_time']
            
            self._print_category_summary(category_results)
        
        overall_results['avg_response_time'] = total_time / overall_results['total_tests'] if overall_results['total_tests'] > 0 else 0
        
        self._print_overall_summary(overall_results)
        return overall_results
    
    def test_basic_commands(self) -> Dict:
        """Test understanding of basic Stata commands"""
        tests = [
            {
                'name': 'Regression command',
                'prompt': 'What does "regress mpg weight length" do in Stata?',
                'expected_keywords': ['regression', 'mpg', 'dependent', 'independent', 'weight', 'length'],
                'forbidden_keywords': []
            },
            {
                'name': 'Summarize command',
                'prompt': 'Explain "summarize price, detail" in Stata',
                'expected_keywords': ['summary', 'statistics', 'detail', 'percentile', 'mean'],
                'forbidden_keywords': []
            },
            {
                'name': 'Generate command',
                'prompt': 'What does "generate newvar = oldvar * 2" do?',
                'expected_keywords': ['create', 'new', 'variable', 'multiply', 'double'],
                'forbidden_keywords': []
            },
            {
                'name': 'Merge command',
                'prompt': 'Explain "merge 1:1 id using dataset2"',
                'expected_keywords': ['merge', 'combine', 'id', 'one-to-one', 'match'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def test_code_explanation(self) -> Dict:
        """Test ability to explain Stata code"""
        tests = [
            {
                'name': 'Loop explanation',
                'prompt': 'Explain this Stata code:\nforeach var of varlist price mpg weight {\n    summarize `var\'\n}',
                'expected_keywords': ['loop', 'iterate', 'each', 'variable', 'summarize'],
                'forbidden_keywords': []
            },
            {
                'name': 'Conditional logic',
                'prompt': 'Explain: replace price = . if price < 0',
                'expected_keywords': ['replace', 'missing', 'conditional', 'negative', 'if'],
                'forbidden_keywords': []
            },
            {
                'name': 'Data transformation',
                'prompt': 'What does this do: bysort company year: egen mean_sales = mean(sales)',
                'expected_keywords': ['group', 'sort', 'average', 'mean', 'company', 'year'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def test_debugging(self) -> Dict:
        """Test ability to identify and fix code issues"""
        tests = [
            {
                'name': 'Missing variable issue',
                'prompt': 'Debug this code: regress price mpg weigth (note: weigth is misspelled)',
                'expected_keywords': ['typo', 'misspell', 'weight', 'variable', 'not found'],
                'forbidden_keywords': []
            },
            {
                'name': 'Syntax error',
                'prompt': 'Fix this: generate newvar = if price > 1000',
                'expected_keywords': ['missing', 'value', 'expression', 'condition', 'syntax'],
                'forbidden_keywords': []
            },
            {
                'name': 'Logic error',
                'prompt': 'What\'s wrong: replace age = 0 if age > 100 (should set to missing)',
                'expected_keywords': ['missing', 'should', 'invalid', 'outlier', 'better'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def test_optimization(self) -> Dict:
        """Test ability to suggest optimizations"""
        tests = [
            {
                'name': 'Inefficient loop',
                'prompt': 'Optimize: foreach i of numlist 1/100 { generate var`i\' = 0 }',
                'expected_keywords': ['efficient', 'better', 'alternative', 'faster', 'reshape'],
                'forbidden_keywords': []
            },
            {
                'name': 'Redundant operations',
                'prompt': 'Improve: sort id\nsort id year\nsort id',
                'expected_keywords': ['redundant', 'unnecessary', 'single', 'once', 'remove'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def test_best_practices(self) -> Dict:
        """Test knowledge of Stata best practices"""
        tests = [
            {
                'name': 'Variable naming',
                'prompt': 'Is "Price_2024" a good Stata variable name? Suggest improvements.',
                'expected_keywords': ['lowercase', 'convention', 'better', 'price_2024', 'underscore'],
                'forbidden_keywords': []
            },
            {
                'name': 'Data preservation',
                'prompt': 'Should I use preserve/restore when making temporary changes?',
                'expected_keywords': ['yes', 'preserve', 'restore', 'temporary', 'revert'],
                'forbidden_keywords': ['no', 'never', 'don\'t']
            },
            {
                'name': 'Missing values',
                'prompt': 'How should I handle missing values before analysis?',
                'expected_keywords': ['check', 'missing', 'drop', 'impute', 'understand'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def test_edge_cases(self) -> Dict:
        """Test handling of edge cases and complex scenarios"""
        tests = [
            {
                'name': 'Complex merge',
                'prompt': 'How do I merge datasets with non-unique identifiers?',
                'expected_keywords': ['many-to-many', 'm:m', 'duplicate', 'careful', 'issue'],
                'forbidden_keywords': []
            },
            {
                'name': 'Panel data',
                'prompt': 'How do I declare panel data structure in Stata?',
                'expected_keywords': ['xtset', 'panel', 'time', 'id', 'declare'],
                'forbidden_keywords': []
            },
        ]
        
        return self._run_tests(tests)
    
    def _run_tests(self, tests: List[Dict]) -> Dict:
        """Run a list of tests and return results"""
        results = {
            'total': len(tests),
            'passed': 0,
            'failed': 0,
            'total_time': 0,
            'tests': []
        }
        
        for test in tests:
            test_result = self._run_single_test(test)
            results['tests'].append(test_result)
            results['total_time'] += test_result['response_time']
            
            if test_result['passed']:
                results['passed'] += 1
                print(f"  ✅ {test['name']}: PASS ({test_result['response_time']:.2f}s)")
            else:
                results['failed'] += 1
                print(f"  ❌ {test['name']}: FAIL ({test_result['response_time']:.2f}s)")
                print(f"     Missing keywords: {test_result['missing_keywords']}")
                if test_result['forbidden_found']:
                    print(f"     Forbidden keywords found: {test_result['forbidden_found']}")
        
        return results
    
    def _run_single_test(self, test: Dict) -> Dict:
        """Run a single test case"""
        start_time = time.time()
        
        try:
            response = self.client.generate(test['prompt'])
            response_time = time.time() - start_time
            
            # Check for expected keywords
            response_lower = response.lower()
            missing_keywords = [kw for kw in test['expected_keywords'] 
                              if kw.lower() not in response_lower]
            
            # Check for forbidden keywords
            forbidden_found = [kw for kw in test.get('forbidden_keywords', [])
                             if kw.lower() in response_lower]
            
            passed = len(missing_keywords) == 0 and len(forbidden_found) == 0
            
            return {
                'name': test['name'],
                'passed': passed,
                'response': response,
                'response_time': response_time,
                'missing_keywords': missing_keywords,
                'forbidden_found': forbidden_found,
                'score': (len(test['expected_keywords']) - len(missing_keywords)) / len(test['expected_keywords']) if test['expected_keywords'] else 1.0
            }
            
        except Exception as e:
            return {
                'name': test['name'],
                'passed': False,
                'response': f"ERROR: {str(e)}",
                'response_time': time.time() - start_time,
                'missing_keywords': test['expected_keywords'],
                'forbidden_found': [],
                'score': 0.0
            }
    
    def _print_category_summary(self, results: Dict):
        """Print summary for a test category"""
        pass_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
        avg_time = results['total_time'] / results['total'] if results['total'] > 0 else 0
        
        print(f"\n  Summary: {results['passed']}/{results['total']} passed ({pass_rate:.1f}%)")
        print(f"  Avg Response Time: {avg_time:.2f}s")
    
    def _print_overall_summary(self, results: Dict):
        """Print overall evaluation summary"""
        print("\n" + "=" * 70)
        print("📊 OVERALL EVALUATION SUMMARY")
        print("=" * 70)
        
        pass_rate = (results['total_passed'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
        
        print(f"\nTotal Tests: {results['total_tests']}")
        print(f"Passed: {results['total_passed']}")
        print(f"Failed: {results['total_tests'] - results['total_passed']}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print(f"Avg Response Time: {results['avg_response_time']:.2f}s")
        
        # Category breakdown
        print("\n📈 Category Performance:")
        for category, cat_results in results['categories'].items():
            cat_pass_rate = (cat_results['passed'] / cat_results['total'] * 100) if cat_results['total'] > 0 else 0
            bar = "█" * int(cat_pass_rate / 10) + "░" * (10 - int(cat_pass_rate / 10))
            print(f"  {category:20s} [{bar}] {cat_pass_rate:5.1f}%")
        
        # Grade
        print(f"\n🎓 Overall Grade: {self._get_grade(pass_rate)}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        self._print_recommendations(results)
    
    def _get_grade(self, pass_rate: float) -> str:
        """Get letter grade from pass rate"""
        if pass_rate >= 90: return "A (Excellent)"
        elif pass_rate >= 80: return "B (Good)"
        elif pass_rate >= 70: return "C (Satisfactory)"
        elif pass_rate >= 60: return "D (Needs Improvement)"
        else: return "F (Poor)"
    
    def _print_recommendations(self, results: Dict):
        """Print improvement recommendations"""
        recommendations = []
        
        for category, cat_results in results['categories'].items():
            pass_rate = (cat_results['passed'] / cat_results['total'] * 100) if cat_results['total'] > 0 else 0
            if pass_rate < 70:
                recommendations.append(f"  ⚠️  Focus on improving {category} (currently {pass_rate:.1f}%)")
        
        if not recommendations:
            print("  ✨ Performance is good across all categories!")
        else:
            for rec in recommendations:
                print(rec)
    
    def save_results(self, filepath: str, results: Dict):
        """Save results to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {filepath}")


def main():
    """Run the evaluation suite"""
    evaluator = StataEvaluator()
    results = evaluator.evaluate_all()
    
    # Save results
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filepath = f"evaluation_results_{timestamp}.json"
    evaluator.save_results(filepath, results)


if __name__ == '__main__':
    main()
