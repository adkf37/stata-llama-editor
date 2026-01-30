"""
Run all tests and generate comprehensive report
"""

import sys
from pathlib import Path
import time
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from test_evaluation import StataEvaluator
from test_performance import PerformanceBenchmark


def main():
    """Run all test suites"""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║         STATA LLAMA EDITOR - COMPREHENSIVE TEST SUITE             ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🕐 Started: {timestamp}\n")
    
    all_results = {
        'timestamp': timestamp,
        'evaluation': None,
        'performance': None
    }
    
    # Run evaluation tests
    try:
        print("\n" + "█" * 70)
        print("PART 1: EVALUATION TESTS")
        print("█" * 70)
        evaluator = StataEvaluator()
        eval_results = evaluator.evaluate_all()
        all_results['evaluation'] = eval_results
    except Exception as e:
        print(f"❌ Evaluation tests failed: {e}")
        all_results['evaluation'] = {'error': str(e)}
    
    # Run performance benchmarks
    try:
        print("\n\n" + "█" * 70)
        print("PART 2: PERFORMANCE BENCHMARKS")
        print("█" * 70)
        benchmark = PerformanceBenchmark()
        perf_results = benchmark.run_all_benchmarks()
        all_results['performance'] = perf_results
    except Exception as e:
        print(f"❌ Performance benchmarks failed: {e}")
        all_results['performance'] = {'error': str(e)}
    
    # Generate report
    print("\n\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "FINAL REPORT" + " " * 36 + "║")
    print("╚" + "═" * 68 + "╝")
    
    generate_report(all_results)
    
    # Save comprehensive results
    save_timestamp = time.strftime('%Y%m%d_%H%M%S')
    filepath = f"comprehensive_test_results_{save_timestamp}.json"
    with open(filepath, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Complete results saved to: {filepath}")
    print(f"\n🕐 Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def generate_report(results: dict):
    """Generate final summary report"""
    print("\n📋 EVALUATION SUMMARY:")
    if 'evaluation' in results and 'error' not in results['evaluation']:
        eval_data = results['evaluation']
        pass_rate = (eval_data['total_passed'] / eval_data['total_tests'] * 100) if eval_data['total_tests'] > 0 else 0
        print(f"   Overall Pass Rate: {pass_rate:.1f}%")
        print(f"   Tests Passed: {eval_data['total_passed']}/{eval_data['total_tests']}")
        print(f"   Grade: {get_grade(pass_rate)}")
    else:
        print("   ❌ Evaluation failed to run")
    
    print("\n⚡ PERFORMANCE SUMMARY:")
    if 'performance' in results and 'error' not in results['performance']:
        perf_data = results['performance']
        if 'latency' in perf_data:
            avg_latencies = [m['avg'] for m in perf_data['latency'].values()]
            overall_avg = sum(avg_latencies) / len(avg_latencies)
            print(f"   Avg Response Time: {overall_avg:.2f}s")
        if 'throughput' in perf_data:
            print(f"   Throughput: {perf_data['throughput']['tokens_per_second']:.1f} tokens/sec")
        if 'streaming' in perf_data:
            print(f"   Time to First Chunk: {perf_data['streaming']['time_to_first_chunk']:.3f}s")
    else:
        print("   ❌ Performance benchmarks failed to run")
    
    print("\n💡 KEY FINDINGS:")
    print_key_findings(results)
    
    print("\n🎯 RECOMMENDATIONS:")
    print_recommendations(results)


def get_grade(pass_rate: float) -> str:
    """Get letter grade"""
    if pass_rate >= 90: return "A (Excellent)"
    elif pass_rate >= 80: return "B (Good)"
    elif pass_rate >= 70: return "C (Satisfactory)"
    elif pass_rate >= 60: return "D (Needs Improvement)"
    else: return "F (Poor)"


def print_key_findings(results: dict):
    """Print key findings"""
    findings = []
    
    # Evaluation findings
    if 'evaluation' in results and 'error' not in results['evaluation']:
        eval_data = results['evaluation']
        pass_rate = (eval_data['total_passed'] / eval_data['total_tests'] * 100) if eval_data['total_tests'] > 0 else 0
        
        if pass_rate >= 80:
            findings.append("   ✅ Strong performance on Stata knowledge tests")
        elif pass_rate >= 60:
            findings.append("   ⚠️  Moderate performance - some areas need improvement")
        else:
            findings.append("   ❌ Significant gaps in Stata knowledge")
        
        # Category-specific findings
        if 'categories' in eval_data:
            for category, cat_data in eval_data['categories'].items():
                cat_rate = (cat_data['passed'] / cat_data['total'] * 100) if cat_data['total'] > 0 else 0
                if cat_rate < 60:
                    findings.append(f"   ⚠️  {category} needs significant improvement ({cat_rate:.0f}%)")
    
    # Performance findings
    if 'performance' in results and 'error' not in results['performance']:
        perf_data = results['performance']
        if 'latency' in perf_data:
            avg_latencies = [m['avg'] for m in perf_data['latency'].values()]
            overall_avg = sum(avg_latencies) / len(avg_latencies)
            
            if overall_avg < 3:
                findings.append("   ✅ Fast response times")
            elif overall_avg < 6:
                findings.append("   ⚠️  Moderate response times")
            else:
                findings.append("   ❌ Slow response times - consider optimization")
    
    if findings:
        for finding in findings:
            print(finding)
    else:
        print("   No key findings available")


def print_recommendations(results: dict):
    """Print recommendations for improvement"""
    recommendations = []
    
    # Evaluation recommendations
    if 'evaluation' in results and 'error' not in results['evaluation']:
        eval_data = results['evaluation']
        if 'categories' in eval_data:
            for category, cat_data in eval_data['categories'].items():
                cat_rate = (cat_data['passed'] / cat_data['total'] * 100) if cat_data['total'] > 0 else 0
                if cat_rate < 70:
                    recommendations.append(f"   • Improve {category} capabilities through targeted training")
    
    # Performance recommendations
    if 'performance' in results and 'error' not in results['performance']:
        perf_data = results['performance']
        if 'latency' in perf_data:
            avg_latencies = [m['avg'] for m in perf_data['latency'].values()]
            overall_avg = sum(avg_latencies) / len(avg_latencies)
            
            if overall_avg > 5:
                recommendations.append("   • Consider using a faster model or optimizing inference")
                recommendations.append("   • Investigate caching frequently asked questions")
        
        if 'throughput' in perf_data:
            tps = perf_data['throughput']['tokens_per_second']
            if tps < 20:
                recommendations.append("   • Low throughput - check hardware resources")
    
    if not recommendations:
        recommendations.append("   ✨ System is performing well! Continue monitoring.")
    
    for rec in recommendations:
        print(rec)


if __name__ == '__main__':
    main()
