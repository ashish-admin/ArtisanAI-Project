// frontend/lib/screens/define_constraints_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/prompt_session_service.dart';
import 'assign_persona_screen.dart';

class DefineConstraintsScreen extends StatefulWidget {
  const DefineConstraintsScreen({super.key});

  @override
  State<DefineConstraintsScreen> createState() => _DefineConstraintsScreenState();
}

class _DefineConstraintsScreenState extends State<DefineConstraintsScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Pre-fill the text field if there's existing data in the session
    _controller.text = Provider.of<PromptSessionService>(context, listen: false).constraints ?? '';
  }

  void _onNext({bool skipped = false}) {
    Provider.of<PromptSessionService>(context, listen: false)
        .setConstraints(skipped ? null : _controller.text);

    // Correctly navigate without passing obsolete arguments
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const AssignPersonaScreen(),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Step 4: Define Constraints')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text(
              'What are the constraints or rules the output must follow?',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'e.g., "The response must be under 100 words..."',
              ),
              maxLines: 5,
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                TextButton(
                  onPressed: () => _onNext(skipped: true),
                  child: const Text('Skip'),
                ),
                ElevatedButton(
                  onPressed: _onNext,
                  child: const Text('Next'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}