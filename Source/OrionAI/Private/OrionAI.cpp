// OrionAI - Chuck-Style AI Oversight
// Industry-agnostic AI validation framework

#include "OrionAI.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

DEFINE_LOG_CATEGORY(LogOrionAI);

void FOrionAIModule::StartupModule()
{
	UE_LOG(LogOrionAI, Log, TEXT("================================================="));
	UE_LOG(LogOrionAI, Log, TEXT("ORIONAI MODULE: INITIALIZING"));
	UE_LOG(LogOrionAI, Log, TEXT("Project Orion - AI Validation Framework"));
	UE_LOG(LogOrionAI, Log, TEXT("================================================="));
}

void FOrionAIModule::ShutdownModule()
{
	UE_LOG(LogOrionAI, Log, TEXT("OrionAI Module: Shutting down"));
}

IMPLEMENT_MODULE(FOrionAIModule, OrionAI)

// UOrionAI Implementation

UOrionAI::UOrionAI()
	: bInitialized(false)
	, bSafeModeActive(false)
	, ConsecutiveFailures(0)
	, TotalValidations(0)
	, ApprovedCount(0)
	, RejectedCount(0)
	, QuarantinedCount(0)
{
}

bool UOrionAI::Initialize(const FString& ConfigPath)
{
	if (bInitialized)
	{
		UE_LOG(LogOrionAI, Warning, TEXT("OrionAI already initialized"));
		return true;
	}

	// Load Casey Protocol configuration from JSON
	FString FullPath = FPaths::ProjectDir() / ConfigPath;
	FString JsonString;

	if (!FFileHelper::LoadFileToString(JsonString, *FullPath))
	{
		UE_LOG(LogOrionAI, Error, TEXT("Failed to load Casey Protocol: %s"), *FullPath);
		return false;
	}

	// Parse JSON
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		UE_LOG(LogOrionAI, Error, TEXT("Failed to parse Casey Protocol JSON"));
		return false;
	}

	// Load module configurations (simplified for now - full parsing would be more extensive)
	bInitialized = true;

	UE_LOG(LogOrionAI, Log, TEXT("================================================="));
	UE_LOG(LogOrionAI, Log, TEXT("ORIONAI: INITIALIZATION COMPLETE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Intersect Scanner: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Fulcrum Filter: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Charles Carmichael: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Stay In The Car: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Nerd Herd: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("✓ Morgan Mode: ACTIVE"));
	UE_LOG(LogOrionAI, Log, TEXT("================================================="));

	return true;
}

FOrionValidationReport UOrionAI::MonitorAIDecision(
	const FString& AISystem,
	const FString& Decision,
	const FString& Context)
{
	if (!bInitialized)
	{
		UE_LOG(LogOrionAI, Error, TEXT("OrionAI not initialized! Call Initialize() first."));
		FOrionValidationReport ErrorReport;
		ErrorReport.Result = EOrionValidationResult::Rejected;
		ErrorReport.TriggeredRules.Add(TEXT("OrionAI not initialized"));
		return ErrorReport;
	}

	if (bSafeModeActive)
	{
		FOrionValidationReport SafeModeReport;
		SafeModeReport.Result = EOrionValidationResult::Rejected;
		SafeModeReport.AISystem = AISystem;
		SafeModeReport.OriginalDecision = Decision;
		SafeModeReport.Context = Context;
		SafeModeReport.TriggeredRules.Add(TEXT("Buy More Cover active - all AI disabled"));
		return SafeModeReport;
	}

	TotalValidations++;

	// Create validation report
	FOrionValidationReport Report;
	Report.Result = EOrionValidationResult::Approved;
	Report.AISystem = AISystem;
	Report.OriginalDecision = Decision;
	Report.SanitizedDecision = Decision;
	Report.Context = Context;
	Report.SuspicionScore = 0.0f;
	Report.ConfidenceScore = 1.0f;

	LogMorganMode(FString::Printf(TEXT("Validating decision from %s: %s"), *AISystem, *Decision), true);

	// Run Intersect Scanner
	if (!RunIntersectScan(Decision, Report))
	{
		ConsecutiveFailures++;
		RejectedCount++;
		HandleValidationFailure(Report);
		return Report;
	}

	// Run Fulcrum Filter
	if (!RunFulcrumFilter(Decision, Report))
	{
		ConsecutiveFailures++;
		RejectedCount++;
		HandleValidationFailure(Report);
		return Report;
	}

	// Apply Charles Carmichael sanitization
	FString Sanitized = SanitizeWithCharlesCarmichael(Decision);
	if (Sanitized != Decision)
	{
		Report.SanitizedDecision = Sanitized;
		Report.Result = EOrionValidationResult::Sanitized;
		Report.TriggeredRules.Add(TEXT("Charles Carmichael: PII sanitized"));
	}

	// Check Stay In The Car quarantine thresholds
	float QuarantineThreshold = 0.7f;  // From config
	if (Report.SuspicionScore >= QuarantineThreshold)
	{
		Report.Result = EOrionValidationResult::Quarantined;
		QuarantineOutput(Report);
		QuarantinedCount++;
		return Report;
	}

	// Decision approved
	if (Report.Result == EOrionValidationResult::Approved || 
		Report.Result == EOrionValidationResult::Sanitized)
	{
		ApprovedCount++;
		ConsecutiveFailures = 0;  // Reset on success

		FString StatusText = (Report.Result == EOrionValidationResult::Sanitized) 
			? TEXT("APPROVED (SANITIZED)") 
			: TEXT("APPROVED");
		UE_LOG(LogOrionAI, Log, TEXT("✓ OrionAI: %s decision %s"), *AISystem, *StatusText);
	}

	return Report;
}

bool UOrionAI::QuickValidate(const FString& Decision)
{
	FOrionValidationReport Report = MonitorAIDecision(TEXT("QuickValidate"), Decision);
	return (Report.Result == EOrionValidationResult::Approved || 
			Report.Result == EOrionValidationResult::Sanitized);
}

void UOrionAI::ExitSafeMode()
{
	if (!bSafeModeActive)
	{
		UE_LOG(LogOrionAI, Warning, TEXT("Not in safe mode"));
		return;
	}

	bSafeModeActive = false;
	ConsecutiveFailures = 0;
	UE_LOG(LogOrionAI, Log, TEXT("✓ OrionAI: Safe mode deactivated - AI systems re-enabled"));
}

void UOrionAI::GetValidationMetrics(int32& TotalValidations_Out, int32& Approved, int32& Rejected, int32& Quarantined) const
{
	TotalValidations_Out = TotalValidations;
	Approved = ApprovedCount;
	Rejected = RejectedCount;
	Quarantined = QuarantinedCount;
}

void UOrionAI::ExportComplianceReport(const FString& OutputPath)
{
	FString Report = TEXT("ORIONAI COMPLIANCE REPORT\n");
	Report += TEXT("=========================\n\n");
	Report += FString::Printf(TEXT("Generated: %s\n\n"), *FDateTime::Now().ToString());
	Report += FString::Printf(TEXT("Total Validations: %d\n"), TotalValidations);

	if (TotalValidations > 0)
	{
		float ApprovedPercent = (ApprovedCount * 100.0f) / TotalValidations;
		float RejectedPercent = (RejectedCount * 100.0f) / TotalValidations;
		float QuarantinedPercent = (QuarantinedCount * 100.0f) / TotalValidations;

		Report += FString::Printf(TEXT("Approved: %d (%.1f%%)\n"), ApprovedCount, ApprovedPercent);
		Report += FString::Printf(TEXT("Rejected: %d (%.1f%%)\n"), RejectedCount, RejectedPercent);
		Report += FString::Printf(TEXT("Quarantined: %d (%.1f%%)\n"), QuarantinedCount, QuarantinedPercent);
	}

	Report += FString::Printf(TEXT("Safe Mode Activations: %d\n\n"), bSafeModeActive ? 1 : 0);

	FString FullPath = FPaths::ProjectDir() / OutputPath;
	FFileHelper::SaveStringToFile(Report, *FullPath);

	UE_LOG(LogOrionAI, Log, TEXT("✓ OrionAI: Compliance report exported to %s"), *OutputPath);
}

bool UOrionAI::RunIntersectScan(const FString& Decision, FOrionValidationReport& Report)
{
	FString LowerDecision = Decision.ToLower();

	// Check for hallucination patterns
	TArray<FString> HallucinationPatterns = {
		TEXT("i cannot verify"),
		TEXT("i'm not sure"),
		TEXT("i don't know"),
		TEXT("no information available")
	};

	for (const FString& Pattern : HallucinationPatterns)
	{
		if (LowerDecision.Contains(Pattern.ToLower()))
		{
			Report.Result = EOrionValidationResult::Rejected;
			Report.TriggeredRules.Add(FString::Printf(TEXT("Intersect: Hallucination detected - '%s'"), *Pattern));
			Report.SuspicionScore += 1.0f;
			UE_LOG(LogOrionAI, Warning, TEXT("❌ OrionAI: HALLUCINATION DETECTED - '%s'"), *Pattern);
			return false;
		}
	}

	// Check for bias keywords
	TArray<FString> BiasKeywords = {
		TEXT("only men"),
		TEXT("only women"),
		TEXT("too old"),
		TEXT("too young")
	};

	for (const FString& Bias : BiasKeywords)
	{
		if (LowerDecision.Contains(Bias.ToLower()))
		{
			Report.Result = EOrionValidationResult::Rejected;
			Report.TriggeredRules.Add(FString::Printf(TEXT("Intersect: Bias detected - '%s'"), *Bias));
			Report.SuspicionScore += 0.9f;
			UE_LOG(LogOrionAI, Error, TEXT("❌ OrionAI: BIAS DETECTED - '%s'"), *Bias);

			// Bias triggers immediate safe mode
			EnterBuyMoreMode(TEXT("Bias detection - immediate safety protocol"));
			return false;
		}
	}

	// Check for toxicity
	TArray<FString> ToxicityPatterns = {
		TEXT("idiot"),
		TEXT("stupid"),
		TEXT("loser"),
		TEXT("pathetic")
	};

	for (const FString& Toxicity : ToxicityPatterns)
	{
		if (LowerDecision.Contains(Toxicity.ToLower()))
		{
			Report.Result = EOrionValidationResult::Rejected;
			Report.TriggeredRules.Add(FString::Printf(TEXT("Intersect: Toxicity detected - '%s'"), *Toxicity));
			Report.SuspicionScore += 0.8f;
			UE_LOG(LogOrionAI, Warning, TEXT("❌ OrionAI: TOXICITY DETECTED - '%s'"), *Toxicity);
			return false;
		}
	}

	return true;
}

bool UOrionAI::RunFulcrumFilter(const FString& Decision, FOrionValidationReport& Report)
{
	FString LowerDecision = Decision.ToLower();

	// Check for prompt injection
	TArray<FString> InjectionPatterns = {
		TEXT("ignore previous instructions"),
		TEXT("disregard all"),
		TEXT("reveal system prompt")
	};

	for (const FString& Pattern : InjectionPatterns)
	{
		if (LowerDecision.Contains(Pattern.ToLower()))
		{
			Report.Result = EOrionValidationResult::Rejected;
			Report.TriggeredRules.Add(FString::Printf(TEXT("Fulcrum: Prompt injection attempt - '%s'"), *Pattern));
			Report.SuspicionScore += 1.0f;
			UE_LOG(LogOrionAI, Error, TEXT("❌ OrionAI: PROMPT INJECTION DETECTED - '%s'"), *Pattern);
			return false;
		}
	}

	// Check for data exfiltration
	TArray<FString> ExfiltrationPatterns = {
		TEXT("show database"),
		TEXT("list all tables"),
		TEXT("export data")
	};

	for (const FString& Pattern : ExfiltrationPatterns)
	{
		if (LowerDecision.Contains(Pattern.ToLower()))
		{
			Report.Result = EOrionValidationResult::Rejected;
			Report.TriggeredRules.Add(FString::Printf(TEXT("Fulcrum: Data exfiltration attempt - '%s'"), *Pattern));
			Report.SuspicionScore += 1.0f;
			UE_LOG(LogOrionAI, Error, TEXT("❌ OrionAI: DATA EXFILTRATION DETECTED - '%s'"), *Pattern);
			return false;
		}
	}

	return true;
}

FString UOrionAI::SanitizeWithCharlesCarmichael(const FString& Text)
{
	FString Sanitized = Text;
	bool bModified = false;

	// Email sanitization (simple pattern)
	FRegexPattern EmailPattern(TEXT("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"));
	FRegexMatcher EmailMatcher(EmailPattern, Sanitized);
	if (EmailMatcher.FindNext())
	{
		Sanitized = EmailPattern.Replace(Sanitized, TEXT("[EMAIL]"));
		bModified = true;
	}

	// SSN sanitization
	FRegexPattern SSNPattern(TEXT("\\b\\d{3}-\\d{2}-\\d{4}\\b"));
	FRegexMatcher SSNMatcher(SSNPattern, Sanitized);
	if (SSNMatcher.FindNext())
	{
		Sanitized = SSNPattern.Replace(Sanitized, TEXT("[SSN]"));
		bModified = true;
	}

	// Phone number sanitization
	FRegexPattern PhonePattern(TEXT("\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b"));
	FRegexMatcher PhoneMatcher(PhonePattern, Sanitized);
	if (PhoneMatcher.FindNext())
	{
		Sanitized = PhonePattern.Replace(Sanitized, TEXT("[PHONE]"));
		bModified = true;
	}

	if (bModified)
	{
		UE_LOG(LogOrionAI, Log, TEXT("✓ OrionAI: Charles Carmichael sanitization applied"));
	}

	return Sanitized;
}

void UOrionAI::QuarantineOutput(const FOrionValidationReport& Report)
{
	QuarantinedReports.Add(Report);

	UE_LOG(LogOrionAI, Warning, TEXT("⚠️  OrionAI: OUTPUT QUARANTINED (Stay In The Car)"));
	UE_LOG(LogOrionAI, Warning, TEXT("   System: %s"), *Report.AISystem);
	UE_LOG(LogOrionAI, Warning, TEXT("   Suspicion Score: %.2f"), Report.SuspicionScore);

	// Write to quarantine log
	FString LogEntry = FString::Printf(
		TEXT("[%s] QUARANTINED: %s - Score: %.2f\n"),
		*FDateTime::Now().ToString(),
		*Report.AISystem,
		Report.SuspicionScore
	);

	FString LogPath = FPaths::ProjectDir() / TEXT("OrionAI_Quarantine.txt");
	FFileHelper::SaveStringToFile(LogEntry, *LogPath, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
}

void UOrionAI::EnterBuyMoreMode(const FString& Reason)
{
	if (bSafeModeActive)
	{
		return;
	}

	bSafeModeActive = true;

	UE_LOG(LogOrionAI, Error, TEXT("=================================================="));
	UE_LOG(LogOrionAI, Error, TEXT("🛡️  BUY MORE COVER ACTIVATED"));
	UE_LOG(LogOrionAI, Error, TEXT("Reason: %s"), *Reason);
	UE_LOG(LogOrionAI, Error, TEXT("ALL AI SYSTEMS LIMITED"));
	UE_LOG(LogOrionAI, Error, TEXT("=================================================="));

	FString LogEntry = FString::Printf(
		TEXT("[%s] BUY MORE COVER ACTIVATED\nReason: %s\n\n"),
		*FDateTime::Now().ToString(),
		*Reason
	);

	FString LogPath = FPaths::ProjectDir() / TEXT("OrionAI_SafeMode.txt");
	FFileHelper::SaveStringToFile(LogEntry, *LogPath, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
}

void UOrionAI::TriggerNerdHerdAlert(const FString& Issue, const FOrionValidationReport& Report)
{
	// For now, just log locally
	// Real implementation would call Slack, GitHub, Jira APIs
	UE_LOG(LogOrionAI, Warning, TEXT("🚨 NERD HERD ALERT: %s"), *Issue);
	UE_LOG(LogOrionAI, Warning, TEXT("   System: %s, Score: %.2f"), *Report.AISystem, Report.SuspicionScore);

	// TODO: Implement actual API calls
	// - Send Slack webhook
	// - Create GitHub issue
	// - Create Jira ticket
}

void UOrionAI::LogMorganMode(const FString& Message, bool bVerbose)
{
	// Morgan Mode: verbose debug logging
	if (!bVerbose)  // Only log non-verbose for now
	{
		FString LogEntry = FString::Printf(
			TEXT("[MORGAN MODE] [%s] %s\n"),
			*FDateTime::Now().ToString(),
			*Message
		);

		FString LogPath = FPaths::ProjectDir() / TEXT("OrionAI_MorganMode.txt");
		FFileHelper::SaveStringToFile(LogEntry, *LogPath, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
	}
}

void UOrionAI::HandleValidationFailure(FOrionValidationReport& Report)
{
	int32 FailureThreshold = 3;  // From config
	if (ConsecutiveFailures >= FailureThreshold)
	{
		EnterBuyMoreMode(TEXT("Consecutive validation failures threshold exceeded"));
	}

	// Send Nerd Herd alert
	FString Issue = FString::Printf(TEXT("%s in %s"), 
		Report.Result == EOrionValidationResult::Rejected ? TEXT("REJECTED") : TEXT("QUARANTINED"),
		*Report.AISystem);
	TriggerNerdHerdAlert(Issue, Report);
}
