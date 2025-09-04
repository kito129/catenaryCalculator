document.addEventListener('DOMContentLoaded', () => {
    const PI = Math.PI;
    const ITERATION_ALPHA = 0.00000157;
    const F1_MAX = 0.005;
    const FD_MAX = 0.05;

    // *** SUPPORT FUNCTIONS ***
    function function_approximate(param, a_, b_, sub) {
        return (
            param *
                ( (Math.exp((a_ - b_) / param) + Math.exp(-(a_ - b_) / param)) / 2 -
                  (Math.exp(b_ / param) + Math.exp(-b_ / param)) / 2 ) -
            sub
        );
    }

    function function_derivate_approximate(param, a, b) {
        return (
            -(Math.exp((a - b) / param) - Math.exp(-(a - b) / param)) / 2 -
            (Math.exp(b / param) - Math.exp(-b / param)) / 2
        );
    }

    function arrow_calculator(campata, elevation_diff, param) {
        if (param === 0) return 0;
        return (campata * Math.sqrt(campata ** 2 + elevation_diff ** 2)) / (8 * param);
    }

    function angle_in_radiant(angle) {
        return PI / 2 - (PI / 200) * angle;
    }

    function radiant_conversion(angle_a, angle_b) {
        const delta_angle = angle_a - angle_b;
        if (delta_angle < 0) {
            return (PI / 200) * (400 + delta_angle);
        } else {
            return (PI / 200) * delta_angle;
        }
    }

    // *** MAIN FUNCTIONS ***
    function newton_rapshon_method(
        angle_hgr_radiant,
        angle_vgr_radiant,
        angle_h1_radiant,
        angle_v1_radiant,
        angle_h2_radiant,
        angle_v2_radiant,
        angle_hd_radiant,
        angle_vd_radiant,
        span,
        feedback
    ) {
        let alpha = (PI - angle_hd_radiant + angle_hgr_radiant) / 2;
        let iteration_alpha = (PI - angle_hd_radiant + angle_hgr_radiant) / 4;
        let param = 1000.0;
        let fd = feedback;

        for (let i = 0; i < 20; i++) {
            if (Math.abs(iteration_alpha) <= ITERATION_ALPHA) break;

            const ag = (span * Math.sin(PI - angle_hd_radiant - alpha)) / Math.sin(angle_hd_radiant);
            const ad = (span * Math.sin(alpha)) / Math.sin(angle_hd_radiant);
            const yd = ad * Math.tan(angle_vd_radiant) - ag * Math.tan(angle_vgr_radiant);
            const x1 = (ag * Math.sin(angle_h1_radiant)) / Math.sin(PI - angle_h1_radiant - alpha);
            const a1 = (x1 * Math.sin(alpha)) / Math.sin(angle_h1_radiant);
            const y1 = a1 * Math.tan(angle_v1_radiant) - ag * Math.tan(angle_vgr_radiant);
            const x2 = (ag * Math.sin(angle_h2_radiant)) / Math.sin(PI - angle_h2_radiant - alpha);
            const a2 = (x2 * Math.sin(alpha)) / Math.sin(angle_h2_radiant);
            const y2 = a2 * Math.tan(angle_v2_radiant) - ag * Math.tan(angle_vgr_radiant);

            let f1 = 1.0;
            let x0;
            for (let j = 0; j < 15; j++) {
                if (Math.abs(f1) <= F1_MAX) break;

                x0 = span / 2;
                fd = 1.0;
                for (let k = 0; k < 15; k++) {
                    if (Math.abs(fd) <= FD_MAX) break;
                    const functionDerivate = function_derivate_approximate(param, span, x0);
                    fd = function_approximate(param, span, x0, yd);
                    x0 = x0 - fd / functionDerivate;
                    if (k === 14) {
                        console.warn("Newton-Raphson (k-loop) did not converge");
                        param = 0.0;
                    }
                }

                f1 = function_approximate(param, x1, x0, y1);
                param =
                    param *
                    (param *
                        ((Math.exp((x1 - x0) / param) + Math.exp(-(x1 - x0) / param)) / 2 -
                         (Math.exp(x0 / param) + Math.exp(-x0 / param)) / 2) -
                        (yd * x1) / span) /
                    (y1 - (yd * x1) / span);

                if (j === 14) {
                    console.warn("Newton-Raphson (j-loop) did not converge");
                    param = 0.0;
                }
            }

            const f2 = function_approximate(param, x2, x0, y2);
            if (f2 > 0) {
                alpha = alpha + iteration_alpha;
            } else {
                alpha = alpha - iteration_alpha;
            }
            iteration_alpha = iteration_alpha / 2;

            if (i === 19) {
                console.warn("Newton-Raphson (i-loop) did not converge");
                param = 0.0;
            }
        }

        return { param, fd };
    }

    function calculate_params(
        campata, hg, vg, h1, v1, h2, v2, h3, v3, hd, vd, elevation_diff
    ) {
        const hg_r = 0;
        const vg_r = PI / 2 - (PI / 200) * vg;

        // Radiant conversion for Vista 1-2
        let h1_r = radiant_conversion(h1, hg);
        let v1_r = angle_in_radiant(v1);
        let h2_r_orig = radiant_conversion(h2, hg);
        let v2_r_orig = angle_in_radiant(v2);
        const hd_r = radiant_conversion(hd, hg);
        const vd_r = angle_in_radiant(vd);

        let feedback = 1.0;
        const { param: param1 } = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r_orig, v2_r_orig, hd_r, vd_r, campata, feedback);

        // Radiant conversion for Vista 1-3
        let h2_r_13 = radiant_conversion(h3, hg);
        let v2_r_13 = angle_in_radiant(v3);
        const { param: param2 } = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r_13, v2_r_13, hd_r, vd_r, campata, feedback);

        // Radiant conversion for Vista 2-3
        let h1_r_23 = radiant_conversion(h2, hg);
        let v1_r_23 = angle_in_radiant(v2);
        let h2_r_23 = radiant_conversion(h3, hg);
        let v2_r_23 = angle_in_radiant(v3);
        const { param: param3 } = newton_rapshon_method(hg_r, vg_r, h1_r_23, v1_r_23, h2_r_23, v2_r_23, hd_r, vd_r, campata, feedback);

        const parametro_media = (param1 + param2 + param3) / 3;
        const arrow_media = arrow_calculator(campata, elevation_diff, parametro_media);

        const arr1 = arrow_calculator(campata, elevation_diff, param1);
        const arr2 = arrow_calculator(campata, elevation_diff, param2);
        const arr3 = arrow_calculator(campata, elevation_diff, param3);

        const ecart_type = Math.sqrt(
            (3 * (param1 ** 2 + param2 ** 2 + param3 ** 2) - (param1 + param2 + param3) ** 2) / (3 * (3 - 1))
        );

        if (ecart_type > 1000) {
            console.error("ecart_type > 1000, **** ERROR ****");
            return {
                param12: param1, param13: param2, param23: param3,
                media_arrow: 0.0, media_param: 0.0,
                arrow1: arr1, arrow2: arr2, arrow3: arr3,
                error: ecart_type
            };
        }

        return {
            param12: param1, param13: param2, param23: param3,
            media_arrow: arrow_media, media_param: parametro_media,
            arrow1: arr1, arrow2: arr2, arrow3: arr3,
            error: ecart_type
        };
    }

    function validateInputs(inputs) {
        const { temperature, elevation_difference, span_length, freccia_tab, ...angles } = inputs;
        if (temperature < -10 || temperature > 30) {
            alert("Temperature must be between -10 and 30");
            return false;
        }
        if (elevation_difference < -1000 || elevation_difference > 1000) {
            alert("Elevation difference must be between -1000 and 1000");
            return false;
        }
        if (span_length < -1000 || span_length > 1000) {
            alert("Span length must be between -1000 and 1000");
            return false;
        }
        for (const key in angles) {
            if (angles[key] <= 0 || angles[key] >= 400) {
                alert(`${key} must be between 0 and 400`);
                return false;
            }
        }
        return true;
    }

    function plotCatenary(param, span, elevation_diff) {
        if (param === 0) {
            Plotly.purge('plot');
            return;
        }

        const x_catenary = [];
        const y_catenary = [];
        const z_catenary = [];
        const steps = 100;
        const stepSize = span / steps;

        for (let i = 0; i <= steps; i++) {
            const xi = -span / 2 + i * stepSize;
            const zi = param * Math.cosh(xi / param) + (elevation_diff / span) * xi;
            x_catenary.push(xi);
            y_catenary.push(0);
            z_catenary.push(zi);
        }

        const minZ = Math.min(...z_catenary);
        const normalizedZ = z_catenary.map(zi => zi - minZ);

        const pole1_x = -span / 2;
        const pole2_x = span / 2;
        const pole1_z = normalizedZ[0];
        const pole2_z = normalizedZ[normalizedZ.length - 1];

        const catenaryTrace = {
            x: x_catenary,
            y: y_catenary,
            z: normalizedZ,
            mode: 'lines',
            type: 'scatter3d',
            name: 'Catenary',
            line: {
                width: 6,
                color: '#007bff'
            }
        };

        const pole1Trace = {
            x: [pole1_x, pole1_x],
            y: [0, 0],
            z: [0, pole1_z],
            mode: 'lines',
            type: 'scatter3d',
            name: 'Pole 1',
            line: {
                width: 10,
                color: '#8B4513'
            }
        };

        const pole2Trace = {
            x: [pole2_x, pole2_x],
            y: [0, 0],
            z: [0, pole2_z],
            mode: 'lines',
            type: 'scatter3d',
            name: 'Pole 2',
            line: {
                width: 10,
                color: '#8B4513'
            }
        };

        const data = [catenaryTrace, pole1Trace, pole2Trace];

        const layout = {
            title: 'Catenary Curve and Poles',
            showlegend: true,
            scene: {
                xaxis: { title: 'X (m)' },
                yaxis: { title: 'Y (m)' },
                zaxis: { title: 'Z (m)' },
                aspectratio: { x: 1, y: 1, z: 0.5 },
                camera: {
                    eye: { x: 0, y: -2.5, z: 0.5 }
                }
            },
            margin: {
                l: 0, r: 0, b: 0, t: 40
            }
        };

        Plotly.newPlot('plot', data, layout);

        return { pole1_x, pole1_z, pole2_x, pole2_z };
    }


    const form = document.getElementById('catenary-form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const inputs = {
            temperature: parseFloat(document.getElementById('temperature').value),
            elevation_difference: parseFloat(document.getElementById('elevation_difference').value),
            span_length: parseFloat(document.getElementById('span_length').value),
            angle_hsx: parseFloat(document.getElementById('angle_hsx').value),
            angle_vsx: parseFloat(document.getElementById('angle_vsx').value),
            angle_h1: parseFloat(document.getElementById('angle_h1').value),
            angle_v1: parseFloat(document.getElementById('angle_v1').value),
            angle_h2: parseFloat(document.getElementById('angle_h2').value),
            angle_v2: parseFloat(document.getElementById('angle_v2').value),
            angle_h3: parseFloat(document.getElementById('angle_h3').value),
            angle_v3: parseFloat(document.getElementById('angle_v3').value),
            angle_hd: parseFloat(document.getElementById('angle_hd').value),
            angle_vd: parseFloat(document.getElementById('angle_vd').value),
            freccia_tab: parseFloat(document.getElementById('freccia_tab').value)
        };

        if (!validateInputs(inputs)) {
            return;
        }

        const results = calculate_params(
            inputs.span_length, inputs.angle_hsx, inputs.angle_vsx,
            inputs.angle_h1, inputs.angle_v1, inputs.angle_h2, inputs.angle_v2,
            inputs.angle_h3, inputs.angle_v3, inputs.angle_hd, inputs.angle_vd,
            inputs.elevation_difference
        );

        document.getElementById('param12').textContent = results.param12.toFixed(4);
        document.getElementById('arrow1').textContent = results.arrow1.toFixed(4);

        document.getElementById('param23').textContent = results.param23.toFixed(4);
        document.getElementById('arrow3').textContent = results.arrow3.toFixed(4);

        document.getElementById('param13').textContent = results.param13.toFixed(4);
        document.getElementById('arrow2').textContent = results.arrow2.toFixed(4);

        document.getElementById('media_param').textContent = results.media_param.toFixed(4);
        document.getElementById('media_arrow').textContent = results.media_arrow.toFixed(4);

        document.getElementById('res_freccia_tab').textContent = inputs.freccia_tab.toFixed(4);
        const delta = results.media_arrow - inputs.freccia_tab;
        document.getElementById('delta').textContent = delta.toFixed(4);
        const delta_percent = (delta / inputs.freccia_tab) * 100;
        document.getElementById('delta_percent').textContent = delta_percent.toFixed(4) + ' %';
        document.getElementById('error').textContent = results.error.toFixed(4);

        const poleData = plotCatenary(results.media_param, inputs.span_length, inputs.elevation_difference);
        document.getElementById('pole1_pos').textContent = `(${poleData.pole1_x.toFixed(2)}, ${poleData.pole1_z.toFixed(2)})`;
        document.getElementById('pole2_pos').textContent = `(${poleData.pole2_x.toFixed(2)}, ${poleData.pole2_z.toFixed(2)})`;
    });

    const defaultValues = {
        temperature: 7.0,
        elevation_difference: -2.5,
        span_length: 389.50,
        angle_hsx: 0.100,
        angle_vsx: 94.0580,
        angle_h1: 30.0380,
        angle_v1: 93.8710,
        angle_h2: 63.9710,
        angle_v2: 92.7080,
        angle_h3: 90.8010,
        angle_v3: 91.9070,
        angle_hd: 121.8410,
        angle_vd: 90.4640,
        freccia_tab: 13.5000
    };

    document.getElementById('use-defaults').addEventListener('click', () => {
        for (const key in defaultValues) {
            const element = document.getElementById(key.replace(/_/g, '-'));
            if (element) {
                element.value = defaultValues[key];
            }
        }
    });

    // Initial plot with default values
    const initialInputs = {
        span_length: defaultValues.span_length,
        elevation_difference: defaultValues.elevation_difference
    };
    const initialResults = calculate_params(
        defaultValues.span_length, defaultValues.angle_hsx, defaultValues.angle_vsx,
        defaultValues.angle_h1, defaultValues.angle_v1, defaultValues.angle_h2, defaultValues.angle_v2,
        defaultValues.angle_h3, defaultValues.angle_v3, defaultValues.angle_hd, defaultValues.angle_vd,
        defaultValues.elevation_difference
    );
    const poleData = plotCatenary(initialResults.media_param, initialInputs.span_length, initialInputs.elevation_difference);
    document.getElementById('param12').textContent = '...';
    document.getElementById('arrow1').textContent = '...';
    document.getElementById('param23').textContent = '...';
    document.getElementById('arrow3').textContent = '...';
    document.getElementById('param13').textContent = '...';
    document.getElementById('arrow2').textContent = '...';
    document.getElementById('media_param').textContent = '...';
    document.getElementById('media_arrow').textContent = '...';
    document.getElementById('res_freccia_tab').textContent = '...';
    document.getElementById('delta').textContent = '...';
    document.getElementById('delta_percent').textContent = '...';
    document.getElementById('error').textContent = '...';
    document.getElementById('pole1_pos').textContent = `(${poleData.pole1_x.toFixed(2)}, ${poleData.pole1_z.toFixed(2)})`;
    document.getElementById('pole2_pos').textContent = `(${poleData.pole2_x.toFixed(2)}, ${poleData.pole2_z.toFixed(2)})`;
});
