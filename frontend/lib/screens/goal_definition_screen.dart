// frontend/lib/screens/goal_definition_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/prompt_session_service.dart';
import 'specify_output_screen.dart';

class GoalDefinitionScreen extends StatefulWidget {
  const GoalDefinitionScreen({super.key});

  @override
  State<GoalDefinitionScreen> createState() => _GoalDefinitionScreenState();
}

class _GoalDefinitionScreenState extends State<GoalDefinitionScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Pre-fill the text field from the session service when the screen loads.
    _controller.text = Provider.of<PromptSessionService>(context, listen: false).goal ?? '';
  }

  void _onNext() {
    if (_controller.text.isNotEmpty) {
      // Save data to the service.
      Provider.of<PromptSessionService>(context, listen: false)
          .setGoal(_controller.text);
      // Navigate cleanly.
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => const SpecifyOutputScreen(),
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Step 1: Define Your Goal')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'What is the primary goal of your prompt? Be as specific as possible.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'e.g., "Generate a marketing email campaign..."',
              ),
              maxLines: 5,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: _onNext,
              child: const Text('Next'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}