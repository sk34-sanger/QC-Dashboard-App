var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.DCC_GraphClickData = function (props) {
    
    const openModal = (e) => {
        e.stopPropagation();
        
        // Create enlarged figure
        const enlargedFigure = props.value ? {
            ...props.value,
            layout: {
                ...props.value.layout,
                width: 800,
                height: 400,
                margin: {l: 50, r: 50, t: 30, b: 50},
                xaxis: {
                    ...props.value.layout.xaxis,
                    showticklabels: true,
                    title: 'Log2(Count + 1)'
                }
            }
        } : null;
        
        // Create modal container
        const modalOverlay = document.createElement('div');
        modalOverlay.id = 'boxplot-modal-' + Date.now();
        modalOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 999999;
        `;
        
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            position: relative;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        `;
        
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '✕';
        closeButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            z-index: 1000000;
        `;
        
        const graphContainer = document.createElement('div');
        graphContainer.id = 'modal-graph-' + Date.now();
        
        const closeModal = () => {
            document.body.removeChild(modalOverlay);
            document.body.style.overflow = '';
        };
        
        closeButton.onclick = closeModal;
        modalOverlay.onclick = closeModal;
        modalContent.onclick = (e) => e.stopPropagation();
        
        modalContent.appendChild(closeButton);
        modalContent.appendChild(graphContainer);
        modalOverlay.appendChild(modalContent);
        document.body.appendChild(modalOverlay);
        document.body.style.overflow = 'hidden';
        
        // Render Plotly graph in the modal
        window.Plotly.newPlot(graphContainer, enlargedFigure.data, enlargedFigure.layout, {
            displayModeBar: true,
            modeBarButtonsToRemove: ['select2d', 'lasso2d'],
            displaylogo: false,
            toImageButtonOptions: {
                format: 'png',
                filename: 'boxplot_enlarged',
                height: 800,
                width: 1600,
                scale: 2
            }
        });
    };
    
    return React.createElement('div', {
        onClick: openModal,
        style: {
            height: '100%',
            width: '100%',
            cursor: 'pointer',
            position: 'relative'
        }
    },
        React.createElement(window.dash_core_components.Graph, {
            figure: props.value,
            style: {height: '100%', width: '100%', pointerEvents: 'none'},
            config: {
                displayModeBar: false,
                staticPlot: true
            }
        })
    );
};