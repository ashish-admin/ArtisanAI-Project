// Path: frontend/lib/widgets/llm_suggestion_card.dart

import 'package:flutter/material.dart';
import 'package:artisan_ai/widgets/educational_tooltip.dart';

class LlmSuggestionCard extends StatelessWidget {
  final Map<String, dynamic> suggestion;

  const LlmSuggestionCard({super.key, required this.suggestion});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8.0),
      color: theme.colorScheme.surface,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.lightbulb_outline, color: theme.colorScheme.secondary),
                const SizedBox(width: 12),
                Text(suggestion['model_name'] ?? 'N/A', style: theme.textTheme.titleLarge),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              suggestion['strengths'] ?? 'No strengths listed.',
              style: theme.textTheme.bodyMedium?.copyWith(fontStyle: FontStyle.italic),
            ),
            const Divider(height: 24),
            Row(
              children: [
                Text('Recommendation Reason', style: theme.textTheme.titleMedium),
                EducationalTooltip(message: suggestion['reason'] ?? 'No reason provided.'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}