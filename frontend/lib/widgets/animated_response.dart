// Path: frontend/lib/widgets/animated_response.dart

import 'package:flutter/material.dart';

class AnimatedResponse extends StatefulWidget {
  final Widget child;
  const AnimatedResponse({super.key, required this.child});

  @override
  _AnimatedResponseState createState() => _AnimatedResponseState();
}

class _AnimatedResponseState extends State<AnimatedResponse>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _animation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeIn,
    );
    _controller.forward();
  }

  @override
  void didUpdateWidget(covariant AnimatedResponse oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.child.key != oldWidget.child.key) {
      _controller.forward(from: 0.0);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: widget.child,
    );
  }
}