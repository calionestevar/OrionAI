// OrionAI.Build.cs
// Build configuration for Unreal Engine integration

using UnrealBuildTool;

public class OrionAI : ModuleRules
{
    public OrionAI(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
        
        PublicIncludePaths.AddRange(
            new string[] {
                // Add public include paths here
            }
        );
        
        PrivateIncludePaths.AddRange(
            new string[] {
                // Add private include paths here
            }
        );
        
        PublicDependencyModuleNames.AddRange(
            new string[]
            {
                "Core",
                "CoreUObject",
                "Engine",
                "Json",
                "JsonUtilities",
                "Http"  // For Nerd Herd API integrations
            }
        );
        
        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
                // Add private dependencies here
            }
        );
        
        DynamicallyLoadedModuleNames.AddRange(
            new string[]
            {
                // Add dynamically loaded modules here
            }
        );
    }
}
