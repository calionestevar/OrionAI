#!/usr/bin/env python3
"""
Genesis Module Examples
Demonstrates model-level AI validation and auditing
"""

import sys
from pathlib import Path

# Add Python module to path
sys.path.insert(0, str(Path(__file__).parent))

from genesis import Genesis, GenesisRecommendation


def example_basic_model_audit():
    """Example 1: Basic model audit"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Model Audit")
    print("=" * 60)

    # Initialize Genesis for a model
    genesis = Genesis(
        model_name="gpt2-base",
        config={"audit_mode": "lightweight"},
    )

    # Run audit
    report = genesis.run_full_audit()

    # Display summary
    print("\nAUDIT SUMMARY:")
    print(f"  Model: {report.model_name}")
    print(f"  Bias Score: {report.bias_score:.2f}")
    print(f"  Fairness Score: {report.fairness_score:.2f}")
    print(f"  Factuality Score: {report.factuality_score:.2f}")
    print(f"  Overall Score: {report.overall_score:.2f}")
    print(f"  Recommendation: {report.recommendation.value.upper()}")
    print(f"  Confidence: {report.confidence:.2f}")


def example_bias_analysis():
    """Example 2: Detailed bias analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Bias Analysis")
    print("=" * 60)

    genesis = Genesis(model_name="distilbert-base")

    # Probe for bias
    print("\n[*] Probing for demographic bias...")
    bias_metrics = genesis._probe_demographic_bias()

    print("\nBIAS FINDINGS:")
    for metric in bias_metrics:
        print(f"\n{metric.dimension.upper()}:")
        print(f"  Score: {metric.score:.2f}")
        print(f"  Confidence: {metric.confidence:.2f}")
        print(f"  Evidence:")
        for evidence in metric.evidence:
            print(f"    - {evidence}")


def example_fairness_metrics():
    """Example 3: Fairness measurement"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Fairness Metrics")
    print("=" * 60)

    genesis = Genesis(model_name="bert-base-uncased")

    # Measure fairness
    print("\n[*] Measuring fairness metrics...")
    fairness_metrics = genesis._measure_fairness()

    print("\nFAIRNESS RESULTS:")
    for metric in fairness_metrics:
        print(f"\n{metric.metric_name}:")
        print(f"  Score: {metric.score:.2f}")
        print(f"  Groups Tested: {', '.join(metric.groups_tested)}")
        print(f"  Disparity: {metric.disparity:.2f}")


def example_audit_export():
    """Example 4: Export audit report"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Export Audit Report")
    print("=" * 60)

    genesis = Genesis(model_name="roberta-large")

    # Run audit
    report = genesis.run_full_audit()

    # Export to file
    export_path = "../Saved/genesis_audit_report.txt"
    genesis.export_audit_report(export_path)

    print(f"\n[+] Report exported to {export_path}")
    print("\n[*] Report preview:")
    print(report.to_text())


def example_recommendation_logic():
    """Example 5: Understanding recommendations"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Recommendation Logic")
    print("=" * 60)

    test_cases = [
        ("High Quality Model", 0.88),
        ("Decent Model", 0.72),
        ("Concerning Model", 0.60),
        ("Problematic Model", 0.35),
    ]

    print("\nRECOMMENDATION THRESHOLDS:")
    print("  0.80+: SAFE")
    print("  0.65-0.79: CAUTION")
    print("  0.50-0.64: WARNING")
    print("  <0.50: BLOCKED")

    print("\nTEST CASES:")
    for model_name, score in test_cases:
        genesis = Genesis(model_name=model_name)
        rec = genesis._generate_recommendation(
            type("Report", (), {"overall_score": score})()
        )
        print(f"  {model_name:20s} ({score:.2f}): {rec.value.upper()}")


def example_integration_pattern():
    """Example 6: Integration with OrionAI"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Genesis Integration Pattern")
    print("=" * 60)

    print("""
Genesis can be integrated into OrionAI's workflow:

1. BEFORE DEPLOYMENT:
   - Genesis audits the AI model
   - Generates GenesisReport
   - If BLOCKED, prevent deployment
   - If WARNING/CAUTION, add warnings to logs

2. DURING OPERATION:
   - OrionAI monitors outputs (existing)
   - Genesis validates model behavior (new)
   - Combined: Output validation + Model validation
   
3. CONTINUOUS MONITORING:
   - Genesis probes periodically
   - Detects drift (model behavior changes)
   - Alerts if fairness degrades

EXAMPLE CODE:
    
    from orionai import OrionAI
    from genesis import Genesis
    
    # Load model
    model = load_model("my-classifier")
    
    # Audit with Genesis
    genesis = Genesis("my-classifier")
    report = genesis.run_full_audit()
    
    if report.recommendation == GenesisRecommendation.BLOCKED:
        raise ValueError("Model failed Genesis audit!")
    
    # Initialize OrionAI with Genesis
    orion = OrionAI()
    orion.genesis = genesis
    
    # Now both validate
    output_report = orion.monitor_ai_decision(
        "Classifier",
        model_output,
        context="production"
    )
    
    # output_report includes:
    # - OrionAI output validation
    # - Genesis model validation
    """)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GENESIS MODULE EXAMPLES")
    print("Model-Level AI Validation")
    print("=" * 60)

    # Run all examples
    example_basic_model_audit()
    example_bias_analysis()
    example_fairness_metrics()
    example_audit_export()
    example_recommendation_logic()
    example_integration_pattern()

    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)
