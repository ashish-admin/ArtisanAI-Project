// Path: frontend/lib/screens/review_prompt_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';
import 'package:artisan_ai/widgets/animated_response.dart';
import 'package:artisan_ai/widgets/custom_card.dart';
import 'package:artisan_ai/widgets/llm_suggestion_card.dart';
import 'package:artisan_ai/widgets/educational_tooltip.dart';

class ReviewPromptScreen extends StatefulWidget {
  const ReviewPromptScreen({super.key});
  @override
  _ReviewPromptScreenState createState() => _ReviewPromptScreenState();
}

class _ReviewPromptScreenState extends State<ReviewPromptScreen> {
  Future<Map<String, dynamic>>? _agentFuture;
  Future<List<dynamic>>? _suggestionsFuture;
  Map<String, dynamic>? _agentResponse;
  final TextEditingController _refinementController = TextEditingController();
  final TextEditingController _saveNameController = TextEditingController();
  bool _isRefining = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _fetchInitialCritique());
  }

  void _fetchInitialCritique() {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    setState(() {
      _agentFuture = sessionService.refinePrompt();
    });
  }

  void _submitRefinement(String sessionId) {
    if (_refinementController.text.isEmpty) return;
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    
    setState(() {
      _isRefining = true;
      _agentFuture = sessionService.submitRefinement(
          sessionId, _refinementController.text);
    });
    _refinementController.clear();
  }

  void _showSaveDialog() {
    // Set default name for the prompt
    _saveNameController.text = Provider.of<PromptSessionService>(context, listen: false).session.goal;

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Save Configuration'),
          content: TextField(
            controller: _saveNameController,
            decoration: const InputDecoration(hintText: "Enter a name for this prompt"),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                if (_saveNameController.text.isNotEmpty) {
                  final sessionService = Provider.of<PromptSessionService>(context, listen: false);
                  final success = await sessionService.saveCurrentSession(
                    name: _saveNameController.text,
                    critiqueText: _agentResponse?['final_critique'],
                    engineeredPrompt: _agentResponse?['engineered_prompt'],
                  );
                  if (mounted) {
                    Navigator.of(context).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(success ? 'Prompt saved successfully!' : 'Failed to save prompt.')),
                    );
                  }
                }
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }

  void _fetchSuggestions() {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    setState(() {
      _suggestionsFuture = sessionService.getLlmSuggestions();
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Review & Refine')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _agentFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('AI is thinking...'),
                ],
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text('An error occurred: ${snapshot.error}', textAlign: TextAlign.center),
              ),
            );
          } else if (snapshot.hasData) {
            _agentResponse = snapshot.data!;
            final isFinal = _agentResponse!['is_final'] ?? false;
            if (isFinal && _suggestionsFuture == null) {
              _fetchSuggestions();
            }
            return AnimatedResponse(
              key: ValueKey(_agentResponse!['session_id']),
              child: isFinal
                  ? _buildFinalCritique(context, _agentResponse!)
                  : _buildConversation(context, _agentResponse!),
            );
          }
          return const Center(child: Text('Something went wrong.'));
        },
      ),
    );
  }

  Widget _buildConversation(BuildContext context, Map<String, dynamic> data) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        CustomCard(
          title: "Agent's Clarification",
          child: Text(data['agent_message'] ?? '...'),
        ),
        const SizedBox(height: 24),
        TextField(
          controller: _refinementController,
          decoration: const InputDecoration(labelText: 'Your Response'),
          keyboardType: TextInputType.multiline,
          maxLines: 3,
        ),
        const SizedBox(height: 16),
        _isRefining
            ? const Center(child: CircularProgressIndicator())
            : ElevatedButton(
                onPressed: () => _submitRefinement(data['session_id']),
                child: const Text('Submit Response'),
              ),
      ],
    );
  }

  Widget _buildFinalCritique(BuildContext context, Map<String, dynamic> data) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        CustomCard(
          title: 'Engineered Prompt',
          titleAction: const EducationalTooltip(
            message: 'This is the prompt our AI engineered based on your input. It is structured to be effective with most advanced LLMs.',
          ),
          action: IconButton(
            icon: const Icon(Icons.copy_all_outlined),
            tooltip: 'Copy Prompt',
            onPressed: () {
              Clipboard.setData(ClipboardData(text: data['engineered_prompt'] ?? ''));
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Prompt copied!')));
            },
          ),
          child: SelectableText(data['engineered_prompt'] ?? 'N/A'),
        ),
        const SizedBox(height: 16),
        CustomCard(
          title: 'AI Generated Critique',
          titleAction: const EducationalTooltip(
            message: 'This is the AI\'s critique of your original request, providing feedback based on the persona you selected.',
          ),
          child: SelectableText(data['final_critique'] ?? 'N/A'),
        ),
        const SizedBox(height: 24),
        Text("Recommended Models", style: Theme.of(context).textTheme.headlineSmall),
        _buildSuggestions(),
        const SizedBox(height: 24),
        ElevatedButton(
          onPressed: _showSaveDialog,
          child: const Text('Save Configuration'),
        ),
      ],
    );
  }

  Widget _buildSuggestions() {
    return FutureBuilder<List<dynamic>>(
      future: _suggestionsFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Padding(padding: EdgeInsets.all(16.0), child: Center(child: CircularProgressIndicator()));
        }
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const SizedBox.shrink(); // Return empty space if no suggestions
        }
        final suggestions = snapshot.data!;
        return Column(
          children: suggestions.map((suggestion) => LlmSuggestionCard(suggestion: suggestion)).toList(),
        );
      },
    );
  }
}