document.addEventListener('DOMContentLoaded', () => {
    const tabGroups = document.querySelectorAll('[data-dashboard-tabs]');
    if (!tabGroups.length) {
        return;
    }

    tabGroups.forEach((tabGroup, groupIndex) => {
        const buttons = Array.from(tabGroup.querySelectorAll('[data-tab-target]'));
        const panels = Array.from(tabGroup.querySelectorAll('.dashboard-tab-panel'));
        const storageKey = `rtd-dashboard-tab-${groupIndex}`;

        const setActiveTab = (targetId, persist = true) => {
            buttons.forEach((button) => {
                const isActive = button.dataset.tabTarget === targetId;
                button.classList.toggle('is-active', isActive);
                button.setAttribute('aria-selected', String(isActive));
                button.tabIndex = isActive ? 0 : -1;
            });

            panels.forEach((panel) => {
                const isActive = panel.id === targetId;
                panel.classList.toggle('is-active', isActive);
                panel.hidden = !isActive;
            });

            if (persist) {
                window.localStorage.setItem(storageKey, targetId);
            }
        };

        buttons.forEach((button) => {
            button.addEventListener('click', () => {
                setActiveTab(button.dataset.tabTarget);
            });
        });

        const savedTarget = window.localStorage.getItem(storageKey);
        const initialButton = buttons.find((button) => button.dataset.tabTarget === savedTarget) || buttons[0];

        if (initialButton) {
            setActiveTab(initialButton.dataset.tabTarget, false);
        }
    });
});
