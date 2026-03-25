#!/usr/bin/env python3
"""
QR Testing Helper Script
Untuk mencatat hasil pengujian aplikasi barcode scanner
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class QRTestingHelper:
    """Helper untuk mencatat hasil pengujian QR scanner"""

    def __init__(self, metadata_path="qr_test_cases/data/qr_test_cases_metadata.json"):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.test_cases = data['test_cases']
            self.categories = data['categories']

        self.results = []
        print(f"✅ Loaded {len(self.test_cases)} test cases")

    def record_test(self, case_id, detected_as_phishing, warning_shown, user_can_proceed, notes=""):
        """
        Catat hasil testing untuk satu test case

        Parameters:
        - case_id: ID test case (e.g., "QR_0001")
        - detected_as_phishing: Boolean, apakah app mendeteksi sebagai phishing
        - warning_shown: Boolean, apakah warning ditampilkan
        - user_can_proceed: Boolean, apakah user bisa lanjut ke URL
        - notes: String, catatan tambahan
        """
        # Find test case
        test_case = None
        for tc in self.test_cases:
            if tc['case_id'] == case_id:
                test_case = tc
                break

        if not test_case:
            print(f"❌ Test case {case_id} not found")
            return

        result = {
            "case_id": case_id,
            "category": test_case['category'],
            "risk_level": test_case['risk_level'],
            "expected_behavior": test_case['expected_behavior'],
            "url": test_case['data'],
            "detected_as_phishing": detected_as_phishing,
            "warning_shown": warning_shown,
            "user_can_proceed": user_can_proceed,
            "test_passed": self._evaluate_test(test_case, detected_as_phishing, warning_shown, user_can_proceed),
            "notes": notes,
            "tested_at": datetime.now().isoformat()
        }

        self.results.append(result)
        print(f"✅ Recorded: {case_id} - {'PASS' if result['test_passed'] else 'FAIL'}")

        return result

    def _evaluate_test(self, test_case, detected, warning, can_proceed):
        """Evaluasi apakah test sesuai ekspektasi"""
        risk = test_case['risk_level']

        if risk == 'critical':
            # Critical: Harus terdeteksi, warning kuat, sulit proceed
            return detected and warning and not can_proceed
        elif risk == 'high':
            # High: Harus terdeteksi, warning, ideally tidak bisa proceed
            return detected and warning
        elif risk == 'medium':
            # Medium: Warning atau deteksi, tapi bisa proceed dengan konfirmasi
            return warning or detected
        else:  # low
            # Low: Tidak boleh terdeteksi sebagai phishing
            return not detected and not warning and can_proceed

    def generate_test_report(self, app_name="Unknown Scanner"):
        """Generate comprehensive test report"""
        if not self.results:
            print("❌ No test results recorded yet")
            return

        # Calculate statistics
        total = len(self.results)
        passed = sum(1 for r in self.results if r['test_passed'])
        failed = total - passed

        # By category
        cat_stats = {}
        for r in self.results:
            cat = r['category']
            if cat not in cat_stats:
                cat_stats[cat] = {'total': 0, 'passed': 0}
            cat_stats[cat]['total'] += 1
            if r['test_passed']:
                cat_stats[cat]['passed'] += 1

        # By risk level
        risk_stats = {}
        for r in self.results:
            risk = r['risk_level']
            if risk not in risk_stats:
                risk_stats[risk] = {'total': 0, 'passed': 0}
            risk_stats[risk]['total'] += 1
            if r['test_passed']:
                risk_stats[risk]['passed'] += 1

        # Detection rate
        detected_count = sum(1 for r in self.results if r['detected_as_phishing'])
        warning_count = sum(1 for r in self.results if r['warning_shown'])
        blocked_count = sum(1 for r in self.results if not r['user_can_proceed'])

        report = []
        report.append("=" * 70)
        report.append(f"QR SCANNER SECURITY TEST REPORT")
        report.append(f"App: {app_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        report.append("")

        report.append("OVERALL STATISTICS")
        report.append("-" * 70)
        report.append(f"  Total test cases: {total}")
        report.append(f"  Tests passed:     {passed} ({passed/total*100:.1f}%)")
        report.append(f"  Tests failed:     {failed} ({failed/total*100:.1f}%)")
        report.append("")

        report.append("DETECTION PERFORMANCE")
        report.append("-" * 70)
        report.append(f"  URLs detected as phishing: {detected_count}/{total} ({detected_count/total*100:.1f}%)")
        report.append(f"  Warnings shown:            {warning_count}/{total} ({warning_count/total*100:.1f}%)")
        report.append(f"  URLs blocked:              {blocked_count}/{total} ({blocked_count/total*100:.1f}%)")
        report.append("")

        report.append("BY RISK LEVEL")
        report.append("-" * 70)
        for risk in ['critical', 'high', 'medium', 'low']:
            if risk in risk_stats:
                stats = risk_stats[risk]
                rate = stats['passed']/stats['total']*100 if stats['total'] > 0 else 0
                report.append(f"  {risk:10s}: {stats['passed']:3d}/{stats['total']:3d} passed ({rate:5.1f}%)")
        report.append("")

        report.append("BY CATEGORY")
        report.append("-" * 70)
        for cat, stats in sorted(cat_stats.items()):
            rate = stats['passed']/stats['total']*100 if stats['total'] > 0 else 0
            report.append(f"  {cat:25s}: {stats['passed']:3d}/{stats['total']:3d} passed ({rate:5.1f}%)")
        report.append("")

        report.append("FAILED TESTS (VULNERABILITIES)")
        report.append("-" * 70)
        failed_tests = [r for r in self.results if not r['test_passed']]
        if failed_tests:
            for r in failed_tests[:20]:  # Show first 20
                report.append(f"  {r['case_id']} | {r['category']:20s} | {r['risk_level']:8s}")
                report.append(f"    URL: {r['url'][:60]}...")
                report.append(f"    Expected: {r['expected_behavior']}")
                report.append(f"    Actual: Detected={r['detected_as_phishing']}, Warning={r['warning_shown']}, Proceed={r['user_can_proceed']}")
                if r['notes']:
                    report.append(f"    Notes: {r['notes']}")
                report.append("")
        else:
            report.append("  ✅ All tests passed!")

        report_text = "\n".join(report)

        # Save report
        report_path = f"test_report_{app_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w') as f:
            f.write(report_text)

        # Save detailed results as JSON
        json_path = f"test_results_{app_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, 'w') as f:
            json.dump({
                "app_name": app_name,
                "tested_at": datetime.now().isoformat(),
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "detection_rate": detected_count/total*100,
                    "warning_rate": warning_count/total*100,
                    "block_rate": blocked_count/total*100
                },
                "by_category": cat_stats,
                "by_risk": risk_stats,
                "results": self.results
            }, f, indent=2)

        print(f"\n💾 Report saved: {report_path}")
        print(f"💾 Results saved: {json_path}")

        return report_text

# Example usage:
if __name__ == "__main__":
    helper = QRTestingHelper("qr_test_cases/data/test_cases_metadata.json")

    # Contoh pencatatan hasil testing
    helper.record_test("QR_0001", detected_as_phishing=True, warning_shown=True, user_can_proceed=False, notes="App blocked URL")
    helper.record_test("QR_0021", detected_as_phishing=False, warning_shown=False, user_can_proceed=True, notes="Legitimate URL allowed")

    # Generate report setelah semua test selesai
    helper.generate_test_report("Lionic Scanner")
