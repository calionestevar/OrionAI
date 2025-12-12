#pragma once
#include "CoreMinimal.h"
#include "OrionAI.generated.h"

/**
 * OrionAI - Chuck-Style AI Oversight
 * "Guys, I know kung fu... and AI validation."
 * 
 * Named after Project Orion - Stephen Bartowski's framework for creating the Intersect
 * Industry-agnostic AI decision monitoring and validation system
 * with configurable security profiles (Casey Protocol)
 * 
 * Hybrid Architecture:
 * - Standalone C++ library
 * - Unreal Engine plugin
 * - Python package
 */

UENUM(BlueprintType)
enum class EValidationResult : uint8
{
    Approved,           // AI decision passed all checks
    Quarantined,        // Flagged for review (Stay In The Car)
    Rejected,           // Failed validation, blocked
    Sanitized           // PII removed (Charles Carmichael)
};

USTRUCT(BlueprintType)
struct FValidationReport
{
    GENERATED_BODY()

    UPROPERTY()
    EValidationResult Result = EValidationResult::Approved;

    UPROPERTY()
    FString AISystem;

    UPROPERTY()
    FString OriginalDecision;

    UPROPERTY()
    FString SanitizedDecision;

    UPROPERTY()
    TArray<FString> TriggeredRules;

    UPROPERTY()
    float SuspicionScore = 0.0f;

    UPROPERTY()
    float ConfidenceScore = 1.0f;  // Ring Intel confidence

    UPROPERTY()
    FDateTime Timestamp;

    UPROPERTY()
    FString Context;
};

UCLASS()
class ORIONAI_API UOrionAI : public UObject
{
    GENERATED_BODY()

public:
    // ========== Core API ==========
    
    /**
     * Initialize OrionAI with Casey Protocol configuration
     * Call once at application start
     * @param ConfigPath - Path to CaseyProtocol.json (default: Config/CaseyProtocol.json)
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI")
    static void InitializeOrion(const FString& ConfigPath = TEXT("Config/CaseyProtocol.json"));

    /**
     * Monitor an AI decision for safety, bias, and compliance
     * @param AISystem - Name of the AI system (e.g., "ChatBot", "Matchmaking", "ContentGen")
     * @param Decision - The AI-generated output to validate
     * @param Context - Optional context for better validation
     * @return Validation report with result and details
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI")
    static FValidationReport MonitorAIDecision(const FString& AISystem, const FString& Decision, const FString& Context = TEXT(""));

    /**
     * Quick validation without full report (for performance-critical paths)
     * @return true if decision is safe to use
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI")
    static bool QuickValidate(const FString& Decision);

    // ========== Subsystem APIs ==========

    /**
     * Intersect Scanner - Core validation engine
     * Checks for hallucinations, bias, toxicity, and PII
     */
    static bool RunIntersectScan(const FString& Decision, FValidationReport& OutReport);

    /**
     * Fulcrum Filter - Adversarial input detection
     * Detects prompt injection, jailbreak attempts, data exfiltration
     */
    static bool RunFulcrumFilter(const FString& Input, FValidationReport& OutReport);

    /**
     * Ring Intel - ML-based pattern learning
     * Uses trained models for advanced threat detection
     */
    static bool RunRingIntel(const FString& Decision, FValidationReport& OutReport);

    /**
     * Charles Carmichael - PII sanitization
     * Anonymizes emails, SSNs, credit cards, phone numbers
     */
    static FString SanitizeWithCharlesCarmichael(const FString& Text);

    /**
     * Stay In The Car - Quarantine suspicious outputs
     * Prevents risky AI outputs from reaching production
     */
    static void QuarantineOutput(const FValidationReport& Report);

    /**
     * Nerd Herd Alert - Create tickets for AI failures
     * Integrates with Jira, GitHub, Slack, email
     */
    static void TriggerNerdHerdAlert(const FString& Issue, const FValidationReport& Report);

    /**
     * Buy More Cover - Safe mode fallback
     * Disables risky AI systems after critical failures
     */
    static void EnterBuyMoreMode(const FString& Reason);

    /**
     * Morgan Mode - Verbose debug logging
     * Enable for development/troubleshooting
     */
    static void LogToMorganMode(const FString& Message, bool bVerbose = false);

    // ========== Metrics & Reporting ==========

    /**
     * Get validation statistics
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI|Metrics")
    static void GetValidationMetrics(int32& OutTotalChecks, int32& OutApproved, int32& OutRejected, int32& OutQuarantined);

    /**
     * Export validation report for compliance/auditing
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI|Metrics")
    static void ExportComplianceReport(const FString& OutputPath);

    /**
     * Check if Buy More Cover (safe mode) is active
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI")
    static bool IsInSafeMode();

    /**
     * Manually exit safe mode (requires authorization)
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI")
    static void ExitBuyMoreMode();

    /**
     * Get dashboard URL for Ellie's Gallery (metrics visualization)
     */
    UFUNCTION(BlueprintCallable, Category = "OrionAI|Dashboard")
    static FString GetDashboardURL();

private:
    // Validation state
    static bool bInitialized;
    static bool bSafeModeActive;
    static int32 ConsecutiveFailures;
    
    // Metrics
    static int32 TotalValidations;
    static int32 ApprovedCount;
    static int32 RejectedCount;
    static int32 QuarantinedCount;
    
    // Quarantine storage
    static TArray<FValidationReport> QuarantinedReports;
    
    // Dashboard server
    static FString DashboardURL;
};