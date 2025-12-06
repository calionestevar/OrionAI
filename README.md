```markdown
# ai-castle — Chuck-Style AI Oversight for Games

**"Yeah, we’ll be there in five… or thirty."**

A standalone, UE5-native AI watchdog that monitors every AI decision in your game — chatbots, NPCs, matchmaking, procedural generation — and answers one question:

> “Is this AI about to get us canceled?”

### Features
- **Intersect Scanner — bias & hallucination detection
- Nerd Herd Auto-Responder — instant ticket creation on AI failure
- Buy More Cover Mode — safe fallback when AI goes rogue
- Zero runtime cost when disabled

### One-Line Activation
```cpp
UAICastle::MonitorAIDecision("ChatBot", GeneratedText);
