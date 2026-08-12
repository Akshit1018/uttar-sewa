import 'package:flutter/material.dart';

import 'app_state.dart';
import 'screens.dart';
import 'widgets.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const UttarSewaApp());
}

class UttarSewaApp extends StatefulWidget {
  const UttarSewaApp({super.key});

  @override
  State<UttarSewaApp> createState() => _UttarSewaAppState();
}

class _UttarSewaAppState extends State<UttarSewaApp> {
  final AppState state = AppState();

  @override
  void initState() {
    super.initState();
    state.addListener(_refresh);
    state.boot();
  }

  void _refresh() => setState(() {});

  @override
  void dispose() {
    state.removeListener(_refresh);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'उत्तर सेवा',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: const ColorScheme.dark(
          primary: Colors.white,
          surface: Color(0xFF111111),
        ),
        scaffoldBackgroundColor: Colors.black,
        useMaterial3: true,
      ),
      home: HomeShell(state: state),
    );
  }
}

class HomeShell extends StatefulWidget {
  const HomeShell({super.key, required this.state});
  final AppState state;

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int index = 0;

  @override
  void initState() {
    super.initState();
    widget.state.addListener(_onAsk);
  }

  @override
  void dispose() {
    widget.state.removeListener(_onAsk);
    super.dispose();
  }

  void _onAsk() {
    if (widget.state.askRequested) {
      widget.state.consumeAskRequest();
      setState(() => index = 0);
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    final pages = [
      ChatScreen(state: state),
      SearchScreen(state: state),
      SadhanaScreen(state: state),
      ControlDashboardScreen(state: state),
      SettingsScreen(state: state),
    ];
    return Scaffold(
      appBar: AppBar(
        title: Text(state.t('उत्तर सेवा', 'Uttar Sewa')),
        actions: [
          TextButton(
            onPressed: () => state.setLanguage(state.isHindi ? 'en' : 'hi'),
            child: Text(state.isHindi ? 'EN' : 'हि'),
          ),
        ],
      ),
      body: Stack(
        children: [
          pages[index],
          if (state.error != null && state.dashboard == null)
            Align(
              alignment: Alignment.topCenter,
              child: Material(
                color: Colors.amber.shade800,
                child: Padding(
                  padding: const EdgeInsets.all(8),
                  child: Text(state.t('API से जुड़ नहीं पाए — बाद में रिफ्रेश करें', 'Could not reach the API — refresh later')),
                ),
              ),
            ),
          JapaOrb(state: state, onAsk: state.openAsk),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (value) => setState(() => index = value),
        destinations: [
          NavigationDestination(icon: const Icon(Icons.chat_bubble_outline), label: state.t('चैट', 'Chat')),
          NavigationDestination(icon: const Icon(Icons.search), label: state.t('खोज', 'Search')),
          NavigationDestination(icon: const Icon(Icons.circle_outlined), label: state.t('साधना', 'Sadhana')),
          NavigationDestination(icon: const Icon(Icons.dashboard_outlined), label: state.t('कंट्रोल', 'Control')),
          NavigationDestination(icon: const Icon(Icons.settings_outlined), label: state.t('सेटिंग', 'Settings')),
        ],
      ),
    );
  }
}
