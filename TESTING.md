# Testing Guide - Stata Llama Editor

## Overview

The test suite evaluates your Stata AI assistant across multiple dimensions to identify strengths and areas for improvement.

## Test Categories

### 1. Evaluation Tests (`test_evaluation.py`)

**What it measures:** Quality and accuracy of Stata-specific responses

**Categories tested:**
- ✅ **Basic Commands** - Understanding of core Stata commands (regress, summarize, generate, merge)
- ✅ **Code Explanation** - Ability to explain Stata code clearly and accurately  
- ✅ **Debugging** - Identifying and fixing code errors and issues
- ✅ **Optimization** - Suggesting more efficient approaches
- ✅ **Best Practices** - Knowledge of Stata conventions and best practices
- ✅ **Edge Cases** - Handling complex scenarios (panel data, complex merges, etc.)

**How it works:**
- Sends test prompts to the AI
- Checks responses for expected keywords (e.g., "regression" for regression questions)
- Validates absence of incorrect information
- Scores each test and calculates category pass rates

**Output:**
- Pass/fail for each test
- Category-level scores
- Overall grade (A-F)
- Specific recommendations for improvement

### 2. Performance Benchmarks (`test_performance.py`)

**What it measures:** Speed and efficiency of the system

**Metrics tracked:**
- ⚡ **Latency** - How long responses take for different query types
  - Short queries (e.g., "What is regress?")
  - Medium queries (explaining concepts)
  - Long queries (complex explanations)

- 📈 **Throughput** - Tokens generated per second
  - Measures generation speed
  - Helps identify hardware bottlenecks

- 🌊 **Streaming** - Real-time response quality
  - Time to first chunk (important for UX)
  - Chunk consistency
  - Total streaming time

- 🔥 **Load Testing** - Performance under multiple requests
  - Sequential request handling
  - Response time stability
  - Standard deviation analysis

**Output:**
- Response time distributions
- Tokens per second metrics
- Performance grade (A-F based on latency)

### 3. Unit Tests (`test_unit.py`)

**What it measures:** Core functionality of individual components

**Components tested:**
- `LlamaClient` - Ollama connection and generation
- `StataHelper` - Code detection and prompt enhancement
- Integration tests - End-to-end flows

**Output:**
- Pass/fail for each unit test
- Pytest format output with detailed error messages

## Running Tests

### Run Everything (Recommended)
```bash
python tests/run_all_tests.py
```

Provides comprehensive report with:
- All evaluation categories
- All performance benchmarks
- Key findings
- Actionable recommendations
- Results saved to JSON file

### Run Individual Test Suites

**Evaluation Only:**
```bash
python tests/test_evaluation.py
```
Best for: Checking content quality improvements

**Performance Only:**
```bash
python tests/test_performance.py
```
Best for: Monitoring system speed and optimizations

**Unit Tests Only:**
```bash
python tests/test_unit.py
```
Best for: Verifying core functionality after code changes

## Interpreting Results

### Evaluation Scores

| Pass Rate | Grade | Interpretation |
|-----------|-------|----------------|
| 90-100% | A | Excellent Stata knowledge |
| 80-89% | B | Good, minor gaps |
| 70-79% | C | Satisfactory, needs work |
| 60-69% | D | Significant gaps |
| Below 60% | F | Major improvements needed |

### Performance Grades

| Avg Latency | Grade | Interpretation |
|-------------|-------|----------------|
| < 2s | A | Very fast |
| 2-4s | B | Fast |
| 4-6s | C | Acceptable |
| 6-10s | D | Slow |
| > 10s | F | Very slow |

### Common Issues & Solutions

**Low Evaluation Scores:**
- ✅ Check if model has sufficient context in prompts
- ✅ Adjust system message in `config.yaml`
- ✅ Consider using larger model (llama3.2:3b vs :1b)
- ✅ Review failed test responses for patterns

**Slow Performance:**
- ✅ Check CPU/RAM usage during tests
- ✅ Reduce `max_tokens` in config if generating too much
- ✅ Consider hardware upgrades
- ✅ Use smaller model if speed is critical

**Inconsistent Results:**
- ✅ Lower `temperature` setting for more deterministic responses
- ✅ Check Ollama server is not under heavy load
- ✅ Review network connectivity if using remote Ollama

## Test Output Files

Tests generate JSON files with detailed results:

```
evaluation_results_YYYYMMDD_HHMMSS.json     # Evaluation test results
comprehensive_test_results_YYYYMMDD_HHMMSS.json  # Complete test suite
```

These files contain:
- All test responses
- Timing data
- Keyword match details
- Recommendations

Use these for:
- Tracking improvements over time
- Sharing results with team
- Deep analysis of specific failures

## Customizing Tests

### Adding New Evaluation Tests

Edit `tests/test_evaluation.py` and add to relevant category:

```python
{
    'name': 'Your test name',
    'prompt': 'Your test prompt',
    'expected_keywords': ['keyword1', 'keyword2'],
    'forbidden_keywords': ['wrong', 'incorrect']
}
```

### Adjusting Test Difficulty

Modify keyword requirements to be more or less strict:
- **More strict:** Add more expected_keywords
- **Less strict:** Reduce expected_keywords
- **Penalize errors:** Add forbidden_keywords

### Custom Benchmarks

Add new performance tests in `test_performance.py`:

```python
def benchmark_your_metric(self) -> Dict:
    # Your benchmark code here
    return results
```

## Best Practices

1. **Run tests regularly** - After any config changes or model updates
2. **Baseline first** - Run tests on initial setup to establish baseline
3. **Track over time** - Keep JSON results to see improvement trends
4. **Focus improvements** - Use category scores to prioritize work
5. **Test in isolation** - Close other apps for accurate performance tests

## Example Test Session

```bash
$ python tests/run_all_tests.py

╔═══════════════════════════════════════════════════════════════════╗
║         STATA LLAMA EDITOR - COMPREHENSIVE TEST SUITE             ║
╚═══════════════════════════════════════════════════════════════════╝

🕐 Started: 2026-01-30 14:30:00

████████████████████████████████████████████████████████████████████
PART 1: EVALUATION TESTS
████████████████████████████████████████████████████████████████████

🧪 Starting Stata Editor Evaluation Suite
======================================================================

📋 Testing: Basic Commands
----------------------------------------------------------------------
  ✅ Regression command: PASS (2.34s)
  ✅ Summarize command: PASS (1.89s)
  ✅ Generate command: PASS (2.01s)
  ...

Overall Grade: B (Good)
💡 Recommendations:
  • Improve Debugging capabilities
  • Optimize response times for complex queries
```

## Support

For issues or questions about testing:
1. Check test output for specific failures
2. Review JSON result files for details
3. Adjust config.yaml settings
4. Consider model size vs. performance tradeoffs
