# An elapsed forecast window becomes history

Method update: October 18, 2026. Proposed experiments below are not reported as executed results.

The screen stores `as_of` and `horizon_days`. The readable CLI and Streamlit view now count rows whose window has elapsed. The original score remains unchanged: an old forecast is evidence of what the rubric said on its as-of date.

The boundary is explicit: a window beginning on its as-of date is historical on as-of plus horizon days. Evaluating the June fixture in October therefore requires an applicability label, even if every source URL remains reachable. URL availability, evidence freshness, horizon applicability and measured calibration answer different questions.

The existing report renderer describes the v0.1 rubric as a deterministic screen. A new report should not promote source-count weights into a calibrated disruption forecast. A useful next dataset records disruptions and non-disruptions for a frozen node cohort, the prediction timestamp and evidence known then. Keep a held-out period for calibration and publish the sample count. Refreshing the forecast requires new dated evidence and a new artifact, with outcomes attached to the historical one.

## References

- https://scikit-learn.org/stable/modules/calibration.html
