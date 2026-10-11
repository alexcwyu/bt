# ffn total-loss numerical compatibility source

Upstream: https://github.com/pmorissette/ffn

PyPI 1.4.1 source archive https://files.pythonhosted.org/packages/b9/b8/19ea55a1db388c8f042f5574e0b053b407a30875e42ba0bcf55e11b9c84c/ffn-1.4.1.tar.gz

Verified SHA256 `470c02fcd8be8a148b8033e9b80fb10ddd8e2102b18b94135c04492e6319779a`. Original license and namespace retained; no upstream tests copied. Local version 1.4.1+ayu1.

Only PerformanceStats log-return evaluation is patched: evaluate log1p for returns greater than -100%; assign negative infinity for exactly -100%, and NaN for undefined values below -100%. This preserves the mathematical output without a NumPy divide/invalid warning for a valid zero-NAV trading result. Refresh from a verified upstream distribution and retire when upstream handles these boundaries. bt's existing complete suite validates the integration.
