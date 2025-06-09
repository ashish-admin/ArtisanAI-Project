// Path: frontend/lib/screens/creation_hub_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/auth_service.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';
import 'package:artisan_ai/widgets/custom_card.dart';

class CreationHubScreen extends StatefulWidget {
  const CreationHubScreen({super.key});

  @override
  _CreationHubScreenState createState() => _CreationHubScreenState();
}

class _CreationHubScreenState extends State<CreationHubScreen> {
  final _goalController = TextEditingController();
  final _contextController = TextEditingController();
  final _personaController = TextEditingController();
  final _constraintsController = TextEditingController();
  String _selectedFormat = 'Text';

  final List<String> _outputFormats = [
    'Text',
    'Email',
    'JSON',
    'Code Snippet',
    'Markdown',
    'Blog Post',
    'Summary'
  ];

  void _onReview() {
    if (_goalController.text.isEmpty || _contextController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('The Goal and Context fields are required.')),
      );
      return;
    }

    final sessionService =
        Provider.of<PromptSessionService>(context, listen: false);

    sessionService.updateGoal(_goalController.text);
    sessionService.updateContext(_contextController.text);
    sessionService.updatePersona(_personaController.text);
    sessionService.updateFormat(_selectedFormat);
    final constraints = _constraintsController.text
        .split(',')
        .map((e) => e.trim())
        .where((e) => e.isNotEmpty)
        .toList();
    sessionService.updateConstraints(constraints);

    Navigator.pushNamed(context, '/review');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Synaptiq // Creation Hub', style: theme.textTheme.titleLarge),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            tooltip: 'Saved Prompts',
            onPressed: () => Navigator.pushNamed(context, '/saved'),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
            onPressed: () {
              Provider.of<AuthService>(context, listen: false).logout();
              Navigator.of(context)
                  .pushNamedAndRemoveUntil('/', (route) => false);
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Describe your objective.', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            Text(
              'Start with a high-level goal. Our AI will help refine it.',
              style: theme.textTheme.bodyMedium?.copyWith(color: Colors.white70),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _goalController,
              decoration: const InputDecoration(
                hintText: 'e.g., "Critique a chapter for plot holes"',
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 32),
            Text('Provide the context.', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            Text(
              'Paste the text, code, or information the AI needs to work with.',
              style: theme.textTheme.bodyMedium?.copyWith(color: Colors.white70),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _contextController,
              decoration: const InputDecoration(
                hintText: 'Your content goes here...',
              ),
              minLines: 10,
              maxLines: 20,
              style: theme.textTheme.bodyLarge?.copyWith(fontFamily: 'monospace'),
            ),
            const SizedBox(height: 32),
            ExpansionTile(
              title: Text('Advanced Parameters', style: theme.textTheme.headlineSmall),
              tilePadding: EdgeInsets.zero,
              children: [
                const SizedBox(height: 16),
                CustomCard(
                  title: 'Output Format',
                  child: Wrap(
                    spacing: 8.0,
                    runSpacing: 4.0,
                    children: _outputFormats.map((format) {
                      return ChoiceChip(
                        label: Text(format),
                        selectedColor: theme.colorScheme.primary,
                        selected: _selectedFormat == format,
                        onSelected: (selected) {
                          setState(() {
                            _selectedFormat = format;
                          });
                        },
                      );
                    }).toList(),
                  ),
                ),
                const SizedBox(height: 16),
                CustomCard(
                  title: 'AI Persona',
                  child: TextField(
                    controller: _personaController,
                    decoration: const InputDecoration(
                        hintText: 'e.g., A skeptical editor, a witty historian'),
                  ),
                ),
                const SizedBox(height: 16),
                CustomCard(
                  title: 'Constraints & Keywords',
                  child: TextField(
                    controller: _constraintsController,
                    decoration: const InputDecoration(
                        hintText: 'e.g., formal, under 200 words, use "synergy"'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 40),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.auto_awesome),
                onPressed: _onReview,
                label: const Text('Engineer & Refine Prompt'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}