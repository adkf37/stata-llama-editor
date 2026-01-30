"""
Performance Benchmarks for Stata Editor
Measures response times and throughput
"""

import sys
from pathlib import Path
import time
import statistics
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llama_client import LlamaClient


class PerformanceBenchmark:
    """Benchmark the performance of the Stata editor"""
    
    def __init__(self):
        self.client = LlamaClient()
    
    def run_all_benchmarks(self) -> Dict:
        """Run all performance benchmarks"""
        print("⚡ Starting Performance Benchmarks\n")
        print("=" * 70)
        
        results = {
            'latency': self.benchmark_latency(),
            'throughput': self.benchmark_throughput(),
            'streaming': self.benchmark_streaming(),
            'load': self.benchmark_load_test()
        }
        
        self._print_summary(results)
        return results
    
    def benchmark_latency(self) -> Dict:
        """Measure response latency for different query types"""
        print("\n📊 Latency Benchmark")
        print("-" * 70)
        
        queries = [
            ("Short query", "What is regress?"),
            ("Medium query", "Explain how to merge two datasets in Stata"),
            ("Long query", "Explain the difference between fixed effects and random effects models in panel data analysis, and when to use each one in Stata"),
        ]
        
        results = {}
        
        for query_type, query in queries:
            times = []
            print(f"\n  Testing: {query_type}")
            
            for i in range(3):
                start = time.time()
                response = self.client.generate(query, max_tokens=200)
                elapsed = time.time() - start
                times.append(elapsed)
                print(f"    Run {i+1}: {elapsed:.2f}s")
            
            results[query_type] = {
                'min': min(times),
                'max': max(times),
                'avg': statistics.mean(times),
                'median': statistics.median(times)
            }
            
            print(f"    Average: {results[query_type]['avg']:.2f}s")
        
        return results
    
    def benchmark_throughput(self) -> Dict:
        """Measure tokens per second"""
        print("\n\n📈 Throughput Benchmark")
        print("-" * 70)
        
        query = "Explain how to perform a multiple regression analysis in Stata, including interpretation of results."
        
        print("\n  Generating response and measuring token throughput...")
        start = time.time()
        response = self.client.generate(query, max_tokens=500)
        elapsed = time.time() - start
        
        # Rough token count (words * 1.3)
        estimated_tokens = len(response.split()) * 1.3
        tokens_per_second = estimated_tokens / elapsed if elapsed > 0 else 0
        
        results = {
            'total_time': elapsed,
            'estimated_tokens': estimated_tokens,
            'tokens_per_second': tokens_per_second
        }
        
        print(f"\n  Total Time: {elapsed:.2f}s")
        print(f"  Estimated Tokens: {estimated_tokens:.0f}")
        print(f"  Throughput: {tokens_per_second:.1f} tokens/sec")
        
        return results
    
    def benchmark_streaming(self) -> Dict:
        """Measure streaming response performance"""
        print("\n\n🌊 Streaming Benchmark")
        print("-" * 70)
        
        query = "Explain Stata's merge command with examples."
        
        print("\n  Testing streaming response...")
        start = time.time()
        chunks = []
        chunk_times = []
        
        first_chunk_time = None
        last_chunk_time = start
        
        for chunk in self.client.stream_generate(query, max_tokens=300):
            current_time = time.time()
            if first_chunk_time is None:
                first_chunk_time = current_time - start
            chunks.append(chunk)
            chunk_times.append(current_time - last_chunk_time)
            last_chunk_time = current_time
        
        total_time = time.time() - start
        
        results = {
            'time_to_first_chunk': first_chunk_time,
            'total_time': total_time,
            'num_chunks': len(chunks),
            'avg_chunk_time': statistics.mean(chunk_times) if chunk_times else 0,
            'total_content_length': sum(len(c) for c in chunks)
        }
        
        print(f"\n  Time to First Chunk: {results['time_to_first_chunk']:.3f}s")
        print(f"  Total Time: {results['total_time']:.2f}s")
        print(f"  Number of Chunks: {results['num_chunks']}")
        print(f"  Avg Chunk Time: {results['avg_chunk_time']:.3f}s")
        
        return results
    
    def benchmark_load_test(self) -> Dict:
        """Test performance under load (sequential requests)"""
        print("\n\n🔥 Load Test (Sequential)")
        print("-" * 70)
        
        num_requests = 5
        query = "What does summarize do?"
        
        print(f"\n  Running {num_requests} requests sequentially...")
        times = []
        
        for i in range(num_requests):
            start = time.time()
            response = self.client.generate(query, max_tokens=100)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"    Request {i+1}: {elapsed:.2f}s")
        
        results = {
            'num_requests': num_requests,
            'total_time': sum(times),
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
        
        print(f"\n  Total Time: {results['total_time']:.2f}s")
        print(f"  Avg per Request: {results['avg_time']:.2f}s")
        print(f"  Std Dev: {results['std_dev']:.2f}s")
        
        return results
    
    def _print_summary(self, results: Dict):
        """Print benchmark summary"""
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 70)
        
        # Latency summary
        print("\n⏱️  Latency:")
        for query_type, metrics in results['latency'].items():
            print(f"  {query_type:15s}: {metrics['avg']:.2f}s avg")
        
        # Throughput
        print(f"\n📈 Throughput: {results['throughput']['tokens_per_second']:.1f} tokens/sec")
        
        # Streaming
        print(f"\n🌊 Streaming: {results['streaming']['time_to_first_chunk']:.3f}s to first chunk")
        
        # Load test
        print(f"\n🔥 Load Test: {results['load']['avg_time']:.2f}s avg per request")
        
        # Performance grade
        avg_latency = statistics.mean([m['avg'] for m in results['latency'].values()])
        print(f"\n🎯 Performance Grade: {self._get_performance_grade(avg_latency)}")
    
    def _get_performance_grade(self, avg_latency: float) -> str:
        """Get performance grade based on average latency"""
        if avg_latency < 2:
            return "A (Excellent) - Very fast responses"
        elif avg_latency < 4:
            return "B (Good) - Fast responses"
        elif avg_latency < 6:
            return "C (Satisfactory) - Acceptable speed"
        elif avg_latency < 10:
            return "D (Slow) - Could be improved"
        else:
            return "F (Very Slow) - Needs optimization"


def main():
    """Run benchmarks"""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()


if __name__ == '__main__':
    main()
