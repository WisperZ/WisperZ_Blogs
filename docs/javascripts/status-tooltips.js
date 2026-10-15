// Zensical's status tooltip subscription can outlive its navigation element.
// Remove only tooltips owned by detached status icons after instant navigation.
(() => {
  let previousStatuses = [];

  function refreshStatusTooltips() {
    for (const status of previousStatuses) {
      if (status.isConnected) continue;

      const ids = (status.getAttribute("aria-describedby") || "")
        .split(/\s+/)
        .filter(Boolean);
      for (const id of ids) {
        const tooltip = document.getElementById(id);
        if (!tooltip?.matches('.md-tooltip2[role="tooltip"]')) continue;

        // An ID shared by an element in the current page is still in use.
        const stillInUse = Array.from(
          document.querySelectorAll("[aria-describedby]"),
        ).some((element) =>
          (element.getAttribute("aria-describedby") || "")
            .split(/\s+/)
            .includes(id),
        );
        if (!stillInUse) tooltip.remove();
      }
    }

    previousStatuses = Array.from(document.querySelectorAll(".md-status"));
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(refreshStatusTooltips);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", refreshStatusTooltips, {
      once: true,
    });
  } else {
    refreshStatusTooltips();
  }
})();
