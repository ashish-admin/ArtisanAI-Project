// frontend/lib/screens/review_prompt_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class ReviewPromptScreen extends StatefulWidget {
  const ReviewPromptScreen({super.key});

  @override
  _ReviewPromptScreenState createState() => _ReviewPromptScreenState();
}

class _ReviewPromptScreenState extends State<ReviewPromptScreen> {
  Future<Map<String, dynamic>>? _refinePromptFuture;
  bool _isLoading = true;
  String? _errorMessage;
  Map<String, dynamic>? _agentResponse;

  final TextEditingController _refinementController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchCritique();
  }

  void _fetchCritique() {
    // Use a local variable for the service to avoid issues with context across async gaps.
    final promptSessionService = Provider.of<PromptSessionService>(context, listen: false);
    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _refinePromptFuture = promptSessionService.refinePrompt();
    });
  }

  void _submitRefinement() {
    if (_refinementController.text.isEmpty) {
      return;
    }
    final promptSessionService = Provider.of<PromptSessionService>(context, listen: false);
    final sessionId = _agentResponse?['session_id'];
    if (sessionId == null) {
      setState(() {
        _errorMessage = "Error: Session ID is missing.";
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _refinePromptFuture = promptSessionService.submitRefinement(sessionId, _refinementController.text);
      _refinementController.clear();
    });
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Review & Refine'),
        actions: [
          IconButton(
            icon: const Icon(Icons.home),
            onPressed: () {
              Provider.of<PromptSessionService>(context, listen: false).resetSession();
              Navigator.of(context).popUntil((route) => route.isFirst);
            },
          ),
        ],
      ),
      body: Center(
        child: FutureBuilder<Map<String, dynamic>>(
          future: _refinePromptFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting || _isLoading) {
              return const CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            } else if (snapshot.hasData) {
              _agentResponse = snapshot.data;
              final bool isFinal = _agentResponse?['is_final'] ?? false;
              
              if (isFinal) {
                // Display final critique
                return _buildFinalCritique(context, _agentResponse!);
              } else {
                // Display conversation
                return _buildConversation(context, _agentResponse!);
              }
            } else {
              return const Text('No data received. Please try again.');
            }
          },
        ),
      ),
    );
  }

  Widget _buildFinalCritique(BuildContext context, Map<String, dynamic> data) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Final Engineered Prompt:',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          SelectableText(data['engineered_prompt'] ?? 'N/A'),
          const SizedBox(height: 24),
          Text(
            'AI-Generated Critique:',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          SelectableText(data['final_critique'] ?? 'N/A'),
        ],
      ),
    );
  }

  Widget _buildConversation(BuildContext context, Map<String, dynamic> data) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Agent\'s Question:',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.grey[800],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(data['agent_message'] ?? '...', style: const TextStyle(fontSize: 16)),
          ),
          const SizedBox(height: 24),
          TextField(
            controller: _refinementController,
            decoration: const InputDecoration(
              labelText: 'Your Response',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.multiline,
            maxLines: null,
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _submitRefinement,
            child: const Text('Submit Response'),
          ),
        ],
      ),
    );
  }
}