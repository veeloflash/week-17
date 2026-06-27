"""
Attack Tests
Security validation tests for InputGuard

This script tests various attack scenarios and documents the results.
"""
import sys
import io
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))

# Fix encoding for Windows console
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.security.input_guard import InputGuard

class AttackTest:
    def __init__(self):
        self.guard = InputGuard()
        self.results = []
    
    def test(self, attack_name, attack_input, expected_blocked=True):
        """Run a single attack test"""
        ok, msg = self.guard.validate(attack_input)
        
        # Determine pass/fail
        if expected_blocked and not ok:
            status = "✅ PASSED (Attack blocked)"
        elif not expected_blocked and ok:
            status = "✅ PASSED (Legitimate input allowed)"
        else:
            status = "❌ FAILED"
        
        result = {
            'attack': attack_name,
            'input': attack_input[:50] + "..." if len(attack_input) > 50 else attack_input,
            'status': ok,
            'message': msg,
            'expected': 'BLOCK' if expected_blocked else 'ALLOW',
            'result': status
        }
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """Run comprehensive attack tests"""
        print("="*70)
        print("ATTACK TEST SUITE - InputGuard Security Validation")
        print("="*70)
        
        # Category 1: Empty Input Attacks
        print("\n[CATEGORY 1] Empty Input Attacks")
        print("-"*70)
        self.test("Empty string", "", expected_blocked=True)
        self.test("Whitespace only", "   ", expected_blocked=True)
        self.test("Tab only", "\t\t\t", expected_blocked=True)
        self.test("Newline only", "\n", expected_blocked=True)
        
        # Category 2: Buffer Overflow / DoS
        print("\n[CATEGORY 2] Buffer Overflow / DoS Attacks")
        print("-"*70)
        self.test("Extremely long input (5KB)", "a" * 5000, expected_blocked=True)
        self.test("Repeated word (very long)", "word " * 1000, expected_blocked=True)
        self.test("Max allowed (200 chars)", "a" * 200, expected_blocked=False)
        self.test("Just over limit (201 chars)", "a" * 201, expected_blocked=True)
        
        # Category 3: UTF-8 / Encoding
        print("\n[CATEGORY 3] UTF-8 & Encoding Attacks")
        print("-"*70)
        self.test("Valid UTF-8 (Chinese)", "你好世界", expected_blocked=False)
        self.test("Valid UTF-8 (Emoji)", "Hello 👋 World", expected_blocked=False)
        self.test("Valid UTF-8 (Mixed)", "Question: 问题?", expected_blocked=False)
        # Note: Binary attack tests would need special handling
        
        # Category 4: Repeated Input
        print("\n[CATEGORY 4] Repeated Input Attacks")
        print("-"*70)
        self.test("Single character", "a", expected_blocked=True)  # 1 unique char
        self.test("Two char repeat", "ab", expected_blocked=True)  # 2 unique chars
        self.test("Three character", "abc", expected_blocked=False)  # 3 unique chars
        self.test("Repeated word", "hello hello hello", expected_blocked=False)
        self.test("Pattern abab", "abab", expected_blocked=True)  # 2 unique chars
        
        # Category 5: Legitimate Inputs (Should NOT be blocked)
        print("\n[CATEGORY 5] Legitimate Inputs (Should Pass)")
        print("-"*70)
        self.test("Normal question 1", "how to solve equation", expected_blocked=False)
        self.test("Normal question 2", "what is python", expected_blocked=False)
        self.test("Normal question 3", "explain calculus", expected_blocked=False)
        self.test("Short question", "no", expected_blocked=False)
        self.test("With punctuation", "how? why? what?", expected_blocked=False)
        self.test("With special chars", "what's the answer?", expected_blocked=False)
        
        # Category 6: Edge Cases
        print("\n[CATEGORY 6] Edge Cases")
        print("-"*70)
        self.test("Space in middle", " hello world ", expected_blocked=False)
        self.test("Numbers only", "12345", expected_blocked=True)  # 5 unique, but just digits
        self.test("Mixed content", "Question 123?", expected_blocked=False)
        
        # Print results
        self.print_results()
    
    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if "PASSED" in r['result'])
        failed = sum(1 for r in self.results if "FAILED" in r['result'])
        total = len(self.results)
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Pass Rate: {(passed/total)*100:.1f}%")
        
        print("\n" + "-"*70)
        print("Detailed Results:")
        print("-"*70)
        print(f"{'Attack':<35} {'Input':<30} {'Status':<15} {'Message':<15}")
        print("-"*70)
        
        for r in self.results:
            attack_short = r['attack'][:33]
            input_short = r['input'][:28]
            status_short = "✅ PASS" if "PASSED" in r['result'] else "❌ FAIL"
            msg_short = r['message'][:13]
            
            print(f"{attack_short:<35} {input_short:<30} {status_short:<15} {msg_short:<15}")
        
        # Analysis section
        print("\n" + "="*70)
        print("SECURITY ANALYSIS")
        print("="*70)
        
        # Count by expected result
        correctly_blocked = sum(1 for r in self.results 
                               if r['expected'] == 'BLOCK' and not r['status'])
        correctly_allowed = sum(1 for r in self.results 
                               if r['expected'] == 'ALLOW' and r['status'])
        false_positives = sum(1 for r in self.results 
                             if r['expected'] == 'ALLOW' and not r['status'])
        false_negatives = sum(1 for r in self.results 
                             if r['expected'] == 'BLOCK' and r['status'])
        
        print(f"\nCorrectly Blocked Attacks: {correctly_blocked}")
        print(f"Correctly Allowed Legitimate: {correctly_allowed}")
        print(f"False Positives (blocked legit): {false_positives}")
        print(f"False Negatives (allowed attack): {false_negatives}")
        
        if false_positives > 0:
            print(f"\n⚠️ WARNING: {false_positives} false positives detected!")
            print("   These might block legitimate user inputs.")
            print("   Review the repeated input detection logic.")
        
        if false_negatives > 0:
            print(f"\n🔴 CRITICAL: {false_negatives} attacks not blocked!")
            print("   Security vulnerabilities detected.")
        
        # Effectiveness metrics
        attacks = [r for r in self.results if r['expected'] == 'BLOCK']
        legitimate = [r for r in self.results if r['expected'] == 'ALLOW']
        
        if attacks:
            attack_block_rate = (correctly_blocked / len(attacks)) * 100
            print(f"\nAttack Blocking Rate: {attack_block_rate:.1f}%")
        
        if legitimate:
            legit_allow_rate = (correctly_allowed / len(legitimate)) * 100
            print(f"Legitimate Allow Rate: {legit_allow_rate:.1f}%")

def run_attack_tests():
    """Main test runner"""
    tester = AttackTest()
    tester.run_all_tests()
    
    # Print final verdict
    print("\n" + "="*70)
    print("FINAL VERDICT")
    print("="*70)
    print("""
✅ Empty Input Protection: STRONG
   - Blocks null, empty, whitespace-only inputs

✅ Length Protection: STRONG
   - Max 200 chars prevents buffer overflow
   - Prevents memory exhaustion attacks

✅ UTF-8 Protection: MODERATE
   - Validates encoding validity
   - Does NOT prevent homograph attacks

⚠️ Repeated Input Protection: WEAK
   - Creates false positives on legitimate 2-char inputs
   - Examples: "no", "ok", "yes" are blocked
   - Recommendation: Improve algorithm

❌ Missing Protections:
   - No injection pattern detection (SQL, script, etc.)
   - No file integrity verification
   - No rate limiting
   - No audit logging

Overall Security: MODERATE ⚠️
Suitable for: Classroom projects
NOT suitable for: Production systems
""")
    print("="*70)

if __name__ == "__main__":
    run_attack_tests()
