"""
Test script for the code analyzer
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.code_analyzer import CodeAnalyzer


def test_local_analysis():
    """Test analyzing the backend code itself."""
    analyzer = CodeAnalyzer()
    
    print("Testing code analyzer with local backend code...")
    print("-" * 60)
    
    # Analyze the backend/app directory
    result = analyzer.analyze_local_directory("app", "test-project")
    
    print(f"\nAnalysis Status: {result['status']}")
    
    if result['status'] == 'completed':
        summary = result['summary']
        print(f"\nProject Summary:")
        print(f"  Total Files: {summary['total_files']}")
        print(f"  Total Classes: {summary['total_classes']}")
        print(f"  Total Functions: {summary['total_functions']}")
        print(f"  Total Imports: {summary['total_imports']}")
        print(f"  Total LOC: {summary['total_loc']}")
        print(f"  Total SLOC: {summary['total_sloc']}")
        print(f"  Comment Ratio: {summary['comment_ratio']:.2%}")
        print(f"  Average Complexity: {summary['average_complexity']}")
        print(f"  Max Complexity: {summary['max_complexity']}")
        print(f"  High Complexity Functions: {summary['high_complexity_count']}")
        
        print(f"\nComplexity Distribution:")
        for rank, count in summary['complexity_distribution'].items():
            print(f"  Rank {rank}: {count} functions")
        
        print(f"\nTop 5 Imported Modules:")
        for imp in result['dependencies']['top_imports'][:5]:
            print(f"  {imp['module']}: {imp['count']} times")
        
        print(f"\nSample Files Analyzed:")
        for file_data in result['files'][:3]:
            print(f"\n  File: {file_data['file_path']}")
            print(f"    Classes: {len(file_data['structure']['classes'])}")
            print(f"    Functions: {len(file_data['structure']['functions'])}")
            print(f"    LOC: {file_data['metrics']['raw'].get('loc', 0)}")
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")
    
    print("\n" + "-" * 60)
    print("Test completed!")


if __name__ == "__main__":
    test_local_analysis()

# Made with Bob
