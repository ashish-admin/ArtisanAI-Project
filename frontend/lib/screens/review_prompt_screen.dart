// Path: frontend/lib/screens/review_prompt_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';
import 'package:artisan_ai/widgets/animated_response.dart';
import 'package:artisan_ai/widgets/custom_card.dart';

class ReviewPromptScreen extends StatefulWidget {
  const ReviewPromptScreen({super.key});

  @override
  _ReviewPromptScreenState createState() => _ReviewPromptScreenState();
}

class _ReviewPromptScreenState extends State<ReviewPromptScreen> {
  Future<Map<String, dynamic>>? _agentFuture;
  Map<String, dynamic>? _agentResponse;
  final TextEditingController _refinementController = TextEditingController();
  bool _isRefining = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _fetchInitialCritique();
    });
  }

  void _fetchInitialCritique() {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    setState(() {
      _agentFuture = sessionService.refinePrompt();
    });
  }

  void _submitRefinement() {
    if (_refinementController.text.isEmpty) return;
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    final sessionId = _agentResponse?['session_id'];

    if (sessionId != null) {
      setState(() {
        _isRefining = true;
        _agentFuture = sessionService.submitRefinement(sessionId, _refinementController.text);
        _refinementController.clear();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Review & Refine'),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _agentFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting && _agentResponse == null) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (snapshot.hasData) {
            _agentResponse = snapshot.data;
          }

          if (_agentResponse == null) {
            return const Center(child: Text('No data received.'));
          }

          final bool isFinal = _agentResponse!['is_final'] ?? false;
          return AnimatedResponse(
            child: isFinal
                ? _buildFinalCritique(_agentResponse!)
                : _buildConversation(_agentResponse!),
          );
        },
      ),
    );
  }

  Widget _buildConversation(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        CustomCard(
          title: "Agent's Clarification",
          child: Text(_agentResponse!['agent_message'] ?? '...'),
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
                onPressed: _submitRefinement,
                child: const Text('Submit Response'),
              ),
      ],
    );
  }

  Widget _buildFinalCritique(BuildContext context) {
    final theme = Theme.of(context);
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        CustomCard(
          title: 'Engineered Prompt',
          child: SelectableText(_agentResponse!['engineered_prompt'] ?? 'N/A'),
          action: IconButton(
            icon: const Icon(Icons.copy_all_outlined),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: _agentResponse!['engineered_prompt'] ?? ''));
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Prompt copied to clipboard!')),
              );
            },
          ),
        ),
        const SizedBox(height: 16),
        CustomCard(
          title: 'AI Generated Critique',
          child: SelectableText(
            _agentResponse!['final_critique'] ?? 'N/A',
            style: theme.textTheme.bodyLarge,
          ),
        ),
      ],
    );
  }
}