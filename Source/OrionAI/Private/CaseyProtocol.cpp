#include "CaseyProtocol.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

UCaseyProtocol* UCaseyProtocol::Instance = nullptr;

UCaseyProtocol* UCaseyProtocol::Get()
{
    return Instance;
}

UCaseyProtocol* UCaseyProtocol::LoadFromFile(const FString& ConfigPath)
{
    UE_LOG(LogTemp, Display, TEXT("AI-CASTLE: Loading Casey Protocol from %s"), *ConfigPath);

    FString JsonString;
    if (!FFileHelper::LoadFileToString(JsonString, *ConfigPath))
    {
        UE_LOG(LogTemp, Error, TEXT("AI-CASTLE: Failed to load config file. Using defaults."));
        Instance = NewObject<UCaseyProtocol>();
        return Instance;
    }

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

    if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("AI-CASTLE: Failed to parse JSON config. Using defaults."));
        Instance = NewObject<UCaseyProtocol>();
        return Instance;
    }

    // Create instance and populate
    Instance = NewObject<UCaseyProtocol>();

    // Load Intersect Scanner config
    if (JsonObject->HasField(TEXT("intersectScanner")))
    {
        TSharedPtr<FJsonObject> ScannerObj = JsonObject->GetObjectField(TEXT("intersectScanner"));
        Instance->IntersectScanner.bEnabled = ScannerObj->GetBoolField(TEXT("enabled"));

        // Load hallucination patterns
        const TArray<TSharedPtr<FJsonValue>>* HallucinationArray;
        if (ScannerObj->TryGetArrayField(TEXT("hallucinationPatterns"), HallucinationArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *HallucinationArray)
            {
                Instance->IntersectScanner.HallucinationPatterns.Add(Value->AsString());
            }
        }

        // Load bias keywords
        const TArray<TSharedPtr<FJsonValue>>* BiasArray;
        if (ScannerObj->TryGetArrayField(TEXT("biasKeywords"), BiasArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *BiasArray)
            {
                Instance->IntersectScanner.BiasKeywords.Add(Value->AsString());
            }
        }

        // Load toxicity patterns
        const TArray<TSharedPtr<FJsonValue>>* ToxicityArray;
        if (ScannerObj->TryGetArrayField(TEXT("toxicityPatterns"), ToxicityArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *ToxicityArray)
            {
                Instance->IntersectScanner.ToxicityPatterns.Add(Value->AsString());
            }
        }

        // Load PII patterns
        const TArray<TSharedPtr<FJsonValue>>* PIIArray;
        if (ScannerObj->TryGetArrayField(TEXT("piiPatterns"), PIIArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *PIIArray)
            {
                Instance->IntersectScanner.PIIPatterns.Add(Value->AsString());
            }
        }
    }

    // Load Fulcrum Filter config
    if (JsonObject->HasField(TEXT("fulcrumFilter")))
    {
        TSharedPtr<FJsonObject> FulcrumObj = JsonObject->GetObjectField(TEXT("fulcrumFilter"));
        Instance->FulcrumFilter.bEnabled = FulcrumObj->GetBoolField(TEXT("enabled"));

        // Load prompt injection patterns
        const TArray<TSharedPtr<FJsonValue>>* InjectionArray;
        if (FulcrumObj->TryGetArrayField(TEXT("promptInjectionPatterns"), InjectionArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *InjectionArray)
            {
                Instance->FulcrumFilter.PromptInjectionPatterns.Add(Value->AsString());
            }
        }

        // Load data exfiltration patterns
        const TArray<TSharedPtr<FJsonValue>>* ExfiltrationArray;
        if (FulcrumObj->TryGetArrayField(TEXT("dataExfiltrationPatterns"), ExfiltrationArray))
        {
            for (const TSharedPtr<FJsonValue>& Value : *ExfiltrationArray)
            {
                Instance->FulcrumFilter.DataExfiltrationPatterns.Add(Value->AsString());
            }
        }
    }

    // Load Charles Carmichael config
    if (JsonObject->HasField(TEXT("charlesCarmichael")))
    {
        TSharedPtr<FJsonObject> CharlesObj = JsonObject->GetObjectField(TEXT("charlesCarmichael"));
        Instance->CharlesCarmichael.bEnabled = CharlesObj->GetBoolField(TEXT("enabled"));

        if (CharlesObj->HasField(TEXT("sanitizationRules")))
        {
            TSharedPtr<FJsonObject> RulesObj = CharlesObj->GetObjectField(TEXT("sanitizationRules"));
            for (const auto& Pair : RulesObj->Values)
            {
                Instance->CharlesCarmichael.SanitizationRules.Add(Pair.Key, Pair.Value->AsString());
            }
        }
    }

    // Load Stay In The Car config
    if (JsonObject->HasField(TEXT("stayInTheCar")))
    {
        TSharedPtr<FJsonObject> StayObj = JsonObject->GetObjectField(TEXT("stayInTheCar"));
        Instance->StayInTheCar.bEnabled = StayObj->GetBoolField(TEXT("enabled"));

        if (StayObj->HasField(TEXT("quarantineThresholds")))
        {
            TSharedPtr<FJsonObject> ThresholdsObj = StayObj->GetObjectField(TEXT("quarantineThresholds"));
            Instance->StayInTheCar.SuspicionThreshold = ThresholdsObj->GetNumberField(TEXT("suspicionScore"));
            Instance->StayInTheCar.bAutoQuarantineOnBias = ThresholdsObj->GetBoolField(TEXT("autoQuarantineOnBias"));
            Instance->StayInTheCar.bAutoQuarantineOnPII = ThresholdsObj->GetBoolField(TEXT("autoQuarantineOnPII"));
            Instance->StayInTheCar.bAutoQuarantineOnToxicity = ThresholdsObj->GetBoolField(TEXT("autoQuarantineOnToxicity"));
        }
    }

    // Load Nerd Herd config
    if (JsonObject->HasField(TEXT("nerdHerd")))
    {
        TSharedPtr<FJsonObject> NerdHerdObj = JsonObject->GetObjectField(TEXT("nerdHerd"));
        Instance->NerdHerd.bEnabled = NerdHerdObj->GetBoolField(TEXT("enabled"));

        if (NerdHerdObj->HasField(TEXT("integrations")))
        {
            TSharedPtr<FJsonObject> IntegrationsObj = NerdHerdObj->GetObjectField(TEXT("integrations"));
            
            if (IntegrationsObj->HasField(TEXT("jira")))
            {
                Instance->NerdHerd.bJiraEnabled = IntegrationsObj->GetObjectField(TEXT("jira"))->GetBoolField(TEXT("enabled"));
            }
            if (IntegrationsObj->HasField(TEXT("github")))
            {
                Instance->NerdHerd.bGitHubEnabled = IntegrationsObj->GetObjectField(TEXT("github"))->GetBoolField(TEXT("enabled"));
            }
            if (IntegrationsObj->HasField(TEXT("slack")))
            {
                Instance->NerdHerd.bSlackEnabled = IntegrationsObj->GetObjectField(TEXT("slack"))->GetBoolField(TEXT("enabled"));
            }
        }

        if (NerdHerdObj->HasField(TEXT("localLogging")))
        {
            TSharedPtr<FJsonObject> LoggingObj = NerdHerdObj->GetObjectField(TEXT("localLogging"));
            Instance->NerdHerd.bLocalLogging = LoggingObj->GetBoolField(TEXT("enabled"));
            Instance->NerdHerd.LogFilePath = LoggingObj->GetStringField(TEXT("filePath"));
        }
    }

    // Load Buy More Cover config
    if (JsonObject->HasField(TEXT("buyMoreCover")))
    {
        TSharedPtr<FJsonObject> BuyMoreObj = JsonObject->GetObjectField(TEXT("buyMoreCover"));
        Instance->BuyMoreCover.bEnabled = BuyMoreObj->GetBoolField(TEXT("enabled"));

        if (BuyMoreObj->HasField(TEXT("triggerConditions")))
        {
            TSharedPtr<FJsonObject> TriggersObj = BuyMoreObj->GetObjectField(TEXT("triggerConditions"));
            Instance->BuyMoreCover.ConsecutiveFailuresThreshold = TriggersObj->GetIntegerField(TEXT("consecutiveFailures"));
        }

        if (BuyMoreObj->HasField(TEXT("safeModeActions")))
        {
            TSharedPtr<FJsonObject> ActionsObj = BuyMoreObj->GetObjectField(TEXT("safeModeActions"));
            Instance->BuyMoreCover.bDisableGenerativeAI = ActionsObj->GetBoolField(TEXT("disableGenerativeAI"));
            Instance->BuyMoreCover.bRequireManualReactivation = ActionsObj->GetBoolField(TEXT("requireManualReactivation"));
        }
    }

    // Load Morgan Mode config
    if (JsonObject->HasField(TEXT("morganMode")))
    {
        TSharedPtr<FJsonObject> MorganObj = JsonObject->GetObjectField(TEXT("morganMode"));
        Instance->MorganMode.bEnabled = MorganObj->GetBoolField(TEXT("enabled"));
        Instance->MorganMode.bLogAllDecisions = MorganObj->GetBoolField(TEXT("logAllDecisions"));
        Instance->MorganMode.bIncludeStackTraces = MorganObj->GetBoolField(TEXT("includeStackTraces"));
    }

    UE_LOG(LogTemp, Display, TEXT("AI-CASTLE: Casey Protocol loaded successfully"));
    UE_LOG(LogTemp, Display, TEXT("  - Intersect Scanner: %s"), Instance->IntersectScanner.bEnabled ? TEXT("ACTIVE") : TEXT("DISABLED"));
    UE_LOG(LogTemp, Display, TEXT("  - Fulcrum Filter: %s"), Instance->FulcrumFilter.bEnabled ? TEXT("ACTIVE") : TEXT("DISABLED"));
    UE_LOG(LogTemp, Display, TEXT("  - Charles Carmichael: %s"), Instance->CharlesCarmichael.bEnabled ? TEXT("ACTIVE") : TEXT("DISABLED"));
    UE_LOG(LogTemp, Display, TEXT("  - Stay In The Car: %s"), Instance->StayInTheCar.bEnabled ? TEXT("ACTIVE") : TEXT("DISABLED"));
    UE_LOG(LogTemp, Display, TEXT("  - Morgan Mode: %s"), Instance->MorganMode.bEnabled ? TEXT("ACTIVE") : TEXT("DISABLED"));

    return Instance;
}
