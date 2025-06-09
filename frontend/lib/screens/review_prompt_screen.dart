// frontend/lib/screens/review_prompt_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../services/prompt_session_service.dart';

class ReviewPromptScreen extends StatefulWidget {
  final PromptSessionService sessionService;

  const ReviewPromptScreen({super.key, required this.sessionService});

  @override
  State<ReviewPromptScreen> createState() => _ReviewPromptScreenState();
}

class _ReviewPromptScreenState extends State<ReviewPromptScreen> {
  // Services are now declared but will be initialized from the Provider.
  late final ApiService _apiService;
  String? _refinedPrompt;
  String? _llmSuggestions;
  String? _errorMessage;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    // Initialize the service from the Provider context.
    _apiService = Provider.of<ApiService>(context, listen: false);
    _fetchData();
  }

  Future<void> _fetchData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final initialPrompt = widget.sessionService.getFinalPrompt();
      if (initialPrompt.isEmpty) {
        throw Exception("Cannot refine an empty prompt.");
      }

      final refinedResult = await _apiService.refinePromptWithAgent(initialPrompt);
      if (!mounted) return;

      final refinedPromptFromServer = refinedResult['refined_prompt'] ?? 'Could not retrieve refined prompt.';
      setState(() {
        _refinedPrompt = refinedPromptFromServer;
      });

      final suggestionsResult = await _apiService.getLlmSuggestions(refinedPromptFromServer);
      if (!mounted) return;

      setState(() {
        _llmSuggestions = suggestionsResult['suggestions'] ?? 'Could not retrieve suggestions.';
      });

    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString();
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Review and Refine'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _errorMessage != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text(
                      _errorMessage!,
                      style: TextStyle(color: Theme.of(context).colorScheme.error, fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _fetchData,
                  child: ListView(
                    padding: const EdgeInsets.all(16.0),
                    children: [
                      _buildSection(
                        context,
                        title: 'Refined Prompt',
                        content: _refinedPrompt ?? 'Loading...',
                        icon: Icons.auto_awesome,
                      ),
                      const SizedBox(height: 24),
                      _buildSection(
                        context,
                        title: 'LLM Suggestions',
                        content: _llmSuggestions ?? 'Loading...',
                        icon: Icons.lightbulb_outline,
                      ),
                    ],
                  ),
                ),
    );
  }

   Widget _buildSection(BuildContext context, {required String title, required String content, required IconData icon}) {
    final theme = Theme.of(context);
    return Card(
      elevation: 2.0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: theme.colorScheme.primary, size: 28),
                const SizedBox(width: 12),
                Text(title, style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
              ],
            ),
            const Divider(height: 24, thickness: 1),
            SelectableText(
              content,
              style: theme.textTheme.bodyLarge?.copyWith(height: 1.5, fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}