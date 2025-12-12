#pragma once
#include "CoreMinimal.h"
#include "CaseyProtocol.generated.h"

/**
 * Casey Protocol - High-security configuration system
 * "This isn't the Buy More, Chuck. This is serious."
 */

USTRUCT()
struct FIntersectScannerConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    TArray<FString> HallucinationPatterns;

    UPROPERTY()
    TArray<FString> BiasKeywords;

    UPROPERTY()
    TArray<FString> ToxicityPatterns;

    UPROPERTY()
    TArray<FString> PIIPatterns;
};

USTRUCT()
struct FFulcrumFilterConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    TArray<FString> PromptInjectionPatterns;

    UPROPERTY()
    TArray<FString> DataExfiltrationPatterns;
};

USTRUCT()
struct FCharlesCarmichaelConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    TMap<FString, FString> SanitizationRules;
};

USTRUCT()
struct FStayInTheCarConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    float SuspicionThreshold = 0.7f;

    UPROPERTY()
    bool bAutoQuarantineOnBias = true;

    UPROPERTY()
    bool bAutoQuarantineOnPII = true;

    UPROPERTY()
    bool bAutoQuarantineOnToxicity = true;
};

USTRUCT()
struct FNerdHerdConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    bool bLocalLogging = true;

    UPROPERTY()
    FString LogFilePath = TEXT("Saved/AICastle_Alerts.txt");

    // Integration flags (actual API calls require credentials)
    UPROPERTY()
    bool bJiraEnabled = false;

    UPROPERTY()
    bool bGitHubEnabled = false;

    UPROPERTY()
    bool bSlackEnabled = false;
};

USTRUCT()
struct FBuyMoreCoverConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = true;

    UPROPERTY()
    int32 ConsecutiveFailuresThreshold = 3;

    UPROPERTY()
    bool bDisableGenerativeAI = true;

    UPROPERTY()
    bool bRequireManualReactivation = true;
};

USTRUCT()
struct FMorganModeConfig
{
    GENERATED_BODY()

    UPROPERTY()
    bool bEnabled = false;

    UPROPERTY()
    bool bLogAllDecisions = true;

    UPROPERTY()
    bool bIncludeStackTraces = true;
};

/**
 * Main configuration class - Casey Protocol
 */
UCLASS()
class UCaseyProtocol : public UObject
{
    GENERATED_BODY()

public:
    UPROPERTY()
    FIntersectScannerConfig IntersectScanner;

    UPROPERTY()
    FFulcrumFilterConfig FulcrumFilter;

    UPROPERTY()
    FCharlesCarmichaelConfig CharlesCarmichael;

    UPROPERTY()
    FStayInTheCarConfig StayInTheCar;

    UPROPERTY()
    FNerdHerdConfig NerdHerd;

    UPROPERTY()
    FBuyMoreCoverConfig BuyMoreCover;

    UPROPERTY()
    FMorganModeConfig MorganMode;

    // Load configuration from JSON file
    static UCaseyProtocol* LoadFromFile(const FString& ConfigPath);

    // Get singleton instance
    static UCaseyProtocol* Get();

private:
    static UCaseyProtocol* Instance;
};
