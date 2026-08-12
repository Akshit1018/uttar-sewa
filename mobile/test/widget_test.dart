import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:uttar_sewa/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({'language': 'hi'});
  });

  testWidgets('shows Hindi title and primary tabs', (tester) async {
    await tester.pumpWidget(const UttarSewaApp());
    await tester.pump();
    expect(find.text('उत्तर सेवा'), findsWidgets);
    expect(find.text('चैट'), findsOneWidget);
    expect(find.text('साधना'), findsOneWidget);
    expect(find.text('कंट्रोल'), findsOneWidget);
    expect(find.text('सेटिंग'), findsOneWidget);
  });

  testWidgets('sadhana tab exposes overlay live activity and watch', (tester) async {
    await tester.pumpWidget(const UttarSewaApp());
    await tester.pump();
    await tester.tap(find.text('साधना'));
    await tester.pumpAndSettle();
    expect(find.text('ओवरले'), findsOneWidget);
    expect(find.text('लाइव गतिविधि'), findsOneWidget);
    expect(find.text('घड़ी'), findsOneWidget);
  });
}
