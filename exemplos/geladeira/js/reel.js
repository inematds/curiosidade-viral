// Reel "Por que a sua geladeira esquenta a sua cozinha" — fotos reais da mesma geladeira + o invisível desenhado por cima.
// Tudo é função do tempo t (evento hf-seek do HyperFrames): sem requestAnimationFrame, sem aleatório.
// Não importa motor/base.js (ele pede ./terra.js, que não vem no motor do kit): os ajudantes estão copiados aqui.
import { FIM, BLOCOS as B, FRASES as F, LEG, palavra } from './tempos.js';

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const io = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const out3 = (k) => 1 - Math.pow(1 - k, 3);
const win = (t, a, b, fin = 0.35, fout = 0.3) => Math.min(out3(ramp(t, a, a + fin)), 1 - ramp(t, b - fout, b));
const $ = (id) => document.getElementById(id);
const NS = 'http://www.w3.org/2000/svg';

// ---------------------------------------------------------------- legenda e cartões (copiados de motor/base.js)
function legenda(t, el = $('leg')) {
  let g = null;
  for (const x of LEG) if (t >= x.ini && t < x.fim) { g = x; break; }
  if (!g) { el.style.opacity = 0; return; }
  const k = out3(ramp(t, g.ini, g.ini + 0.14)), sai = 1 - ramp(t, g.fim - 0.1, g.fim);
  if (el.dataset.txt !== g.txt) {
    el.dataset.txt = g.txt;
    el.innerHTML = g.txt.split(' ').map((p) => {
      const limpo = p.replace(/[?!.,:]$/, '');
      return g.quente.includes(limpo) || g.quente.includes(p) ? `<b>${p}</b>` : p;
    }).join(' ');
  }
  el.style.opacity = Math.min(k, sai);
  el.style.transform = `translate(-50%, ${(1 - k) * 14}px) scale(${0.94 + 0.06 * k})`;
}
function quando(spec) {
  if (/^[\d.]+$/.test(spec.trim())) return Number(spec);
  const m = /^([\w-]+)(?:\.(ini|fim))?([+-][\d.]+)?$/.exec(spec.trim());
  if (!m) return Number(spec);
  const base = F[m[1]] || B[m[1]]; if (!base) { console.warn('tempo desconhecido', spec); return 0; }
  return base[m[2] || 'ini'] + (m[3] ? Number(m[3]) : 0);
}
let cartoesDOM = null;
function cartoes(t) {
  if (!cartoesDOM) cartoesDOM = [...document.querySelectorAll('[data-de]')].map((el) => ({ el, de: quando(el.dataset.de), ate: el.dataset.ate ? quando(el.dataset.ate) : 1e9 }));
  for (const c of cartoesDOM) {
    c.el.style.opacity = win(t, c.de, c.ate, 0.35, 0.25);
    c.el.style.transform = `translateY(${(1 - out3(ramp(t, c.de, c.de + 0.35))) * 22}px)`;
  }
}

// ---------------------------------------------------------------- relógio da história
const corte = (b) => B[b].ini - 0.12;
const T = {
  esquenta: palavra('g', 'esquenta'),
  esquenta1: palavra('f1', 'esquenta'),
  calor3: palavra('f3', 'calor'),
  grade4: palavra('f4', 'grade'),
  motor: palavra('f5', 'motor'),
  tomada: palavra('f5', 'tomada'),
  junto: palavra('f6', 'junto'),
  cozinha7: palavra('f7', 'cozinha'),
  aquecedor: palavra('f8', 'aquecedor'),
  f6: F.f6.ini - 0.12,
  f8: F.f8.ini - 0.12,
  toque: F.f9.fim - 0.35,
};

// Cada foto: os intervalos em que está na tela. A que entrou por último fica por cima (dissolve de 0,3 s).
const FOTOS = {
  frente: [[-1, corte('b1') + 0.3], [T.f8, 1e9]],
  aberta: [[corte('b1'), corte('b3') + 0.3], [corte('b5'), T.f8 + 0.3]],
  tras: [[corte('b3'), T.f6 + 0.3]],
  grade: [[T.f6, corte('b5') + 0.3]],
};
function fotos(t) {
  for (const [nome, ivs] of Object.entries(FOTOS)) {
    const el = $('im-' + nome);
    let op = 0, ini = -2;
    for (const [a, b] of ivs) if (t >= a && t < b) { op = a < 0 ? 1 : out3(ramp(t, a, a + 0.3)); ini = a; }
    el.style.opacity = op;
    el.style.zIndex = op > 0 ? Math.round((ini + 2) * 10) : 0;
  }
}

// Câmera: pontos (t, cx, cy, z) no espaço da foto (1080×1920). Dois pontos no mesmo t = corte. z ≤ 1,25.
const CAM = [
  [0, 540, 960, 1.0], [corte('b1'), 540, 930, 1.07],
  [corte('b1'), 560, 960, 1.0], [B.b1.fim, 560, 960, 1.04],
  [T.calor3 + 0.4, 440, 960, 1.2], [corte('b3'), 450, 950, 1.23],
  [corte('b3'), 600, 960, 1.0], [T.grade4 + 0.6, 640, 820, 1.12], [corte('b4'), 650, 830, 1.13],
  [T.motor + 0.3, 600, 1120, 1.2], [T.f6, 600, 1120, 1.21],
  [T.f6, 540, 960, 1.0], [corte('b5'), 560, 930, 1.12],
  [corte('b5'), 540, 960, 1.0], [T.f8, 540, 960, 1.06],
  [T.f8, 540, 960, 1.0], [B.b6.ini, 540, 960, 1.05], [FIM + 1, 540, 960, 1.05],
];
function camera(t) {
  let i = 0;
  while (i < CAM.length - 2 && t >= CAM[i + 1][0]) i++;
  const [ta, xa, ya, za] = CAM[i], [tb, xb, yb, zb] = CAM[i + 1];
  const k = tb > ta ? io(ramp(t, ta, tb)) : 1;
  let cx = lerp(xa, xb, k), cy = lerp(ya, yb, k), z = lerp(za, zb, k);
  cx = clamp(cx, 540 / z, 1080 - 540 / z); cy = clamp(cy, 960 / z, 1920 - 960 / z); // nunca mostra a borda da foto
  $('palco').style.transform = `translate(${540 - cx * z}px, ${960 - cy * z}px) scale(${z})`;
}

// ---------------------------------------------------------------- o invisível
// Onda de calor: um trecho ondulado que sobe sem parar (posição = função de t), cor do calor, some nas pontas.
function ondaPath(x, y, len, amp, fase) {
  let d = `M${x + Math.sin(fase) * amp},${y}`;
  for (let s = 1; s <= 24; s++) { const yy = y - (len * s) / 24; d += ` L${(x + Math.sin(fase + s * 0.55) * amp).toFixed(1)},${yy.toFixed(1)}`; }
  return d;
}
// grupos de ondas: x, faixa vertical [yTopo, yBase], comprimento, quantas, largura do traço
function grupo(xs, yTopo, yBase, len, larg, sem) {
  return xs.map((x, i) => ({ x, yTopo, yBase, len, larg, sem: sem + i * 1.7 }));
}
const ONDAS = {
  frente: [...grupo([60, 130, 950, 1020], 120, 1760, 420, 9, 0.3)],
  aberta: [...grupo([50, 115, 175], 60, 1500, 400, 9, 2.1), ...grupo([300, 480, 660], -200, 60, 260, 8, 4.4)],
  tras: [...grupo([420, 520, 620, 720, 820, 920], 0, 1500, 380, 10, 1.2)],
  grade: [...grupo([120, 260, 400, 540, 680, 820, 960], -100, 1900, 480, 12, 5.0)],
  volta: [...grupo([40, 100, 160], 0, 1600, 460, 11, 3.3), ...grupo([260, 420, 580, 740], -260, 40, 300, 10, 6.1)],
  fim: [...grupo([40, 110, 180, 900, 970, 1040], 60, 1800, 480, 11, 7.7)],
};
const ondasEl = {};
for (const [nome, lista] of Object.entries(ONDAS)) {
  const g = document.createElementNS(NS, 'g'); $('ondas').appendChild(g);
  ondasEl[nome] = { g, paths: lista.map((o) => { const p = document.createElementNS(NS, 'path'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', 'url(#gCalor)'); p.setAttribute('stroke-width', o.larg); p.setAttribute('stroke-linecap', 'round'); g.appendChild(p); return { p, o }; }) };
}
function ondas(t, nome, op, vel = 150) {
  const { g, paths } = ondasEl[nome];
  g.style.opacity = op;
  if (op <= 0.001) return;
  for (const { p, o } of paths) {
    const span = o.yBase - o.yTopo + o.len;
    const y = o.yBase - (((t * vel + o.sem * 173) % span) + span) % span + o.len * 0.5;
    p.setAttribute('d', ondaPath(o.x, y, o.len, 14, t * 3.1 + o.sem));
  }
}

// setas de fluxo (tracejado que anda): calor de dentro para o fundo; frio que escorre pela porta; energia da tomada
function seta(pai, d, cor, larg, ponta) {
  const p = document.createElementNS(NS, 'path');
  p.setAttribute('d', d); p.setAttribute('fill', 'none'); p.setAttribute('stroke', cor); p.setAttribute('stroke-width', larg);
  p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-dasharray', '34 22'); if (ponta) p.setAttribute('marker-end', `url(#${ponta})`);
  pai.appendChild(p); return p;
}
const gDentro = document.createElementNS(NS, 'g'); $('setas').appendChild(gDentro);
const SETAS_DENTRO = [
  'M240,820 Q330,700 430,610', 'M260,1080 Q360,860 435,640', 'M560,860 Q520,720 450,620', 'M590,1130 Q560,860 455,650', 'M800,760 Q640,640 470,600',
].map((d) => seta(gDentro, d, '#ff5a2a', 11, 'pontaC'));
const gSobe = document.createElementNS(NS, 'g'); $('setas').appendChild(gSobe);
const SETA_SOBE = seta(gSobe, 'M445,590 L445,380', '#ff5a2a', 14, 'pontaC');
const gFrio = document.createElementNS(NS, 'g'); $('frio').appendChild(gFrio);
const SETAS_FRIO = ['M360,1330 Q300,1560 200,1760', 'M470,1350 Q470,1580 430,1800', 'M600,1340 Q660,1560 700,1780', 'M760,1280 Q860,1500 900,1700']
  .map((d) => seta(gFrio, d, '#8fd3ff', 10, 'pontaF'));
const gLuz = document.createElementNS(NS, 'g'); $('setas').appendChild(gLuz);
const SETA_LUZ = seta(gLuz, 'M200,1900 Q330,1760 470,1700', '#ffffff', 8, null);

// rótulos: só o nome, linha fina até a peça
function rotulo(texto, x, y, x2, y2, cor = '#fff') {
  const g = document.createElementNS(NS, 'g'); $('rotulos').appendChild(g);
  const l = document.createElementNS(NS, 'line');
  Object.entries({ x1: x, y1: y + 10, x2, y2, stroke: cor, 'stroke-width': 3 }).forEach(([k, v]) => l.setAttribute(k, v));
  const c = document.createElementNS(NS, 'circle');
  Object.entries({ cx: x2, cy: y2, r: 8, fill: cor }).forEach(([k, v]) => c.setAttribute(k, v));
  const tx = document.createElementNS(NS, 'text');
  Object.entries({ x, y, class: 'rot', 'text-anchor': 'middle' }).forEach(([k, v]) => tx.setAttribute(k, v));
  tx.textContent = texto; tx.setAttribute('fill', cor);
  g.append(l, c, tx); g.style.opacity = 0; return g;
}
const R_CONDENSADOR = rotulo('CONDENSADOR', 560, 560, 650, 700);
const R_MOTOR = rotulo('MOTOR', 330, 1440, 560, 1640);
// "refresca?" riscado de vermelho: o que a pessoa acha (errado)
const R_REFRESCA = (() => {
  const g = document.createElementNS(NS, 'g'); $('rotulos').appendChild(g);
  const tx = document.createElementNS(NS, 'text');
  Object.entries({ x: 470, y: 1250, 'text-anchor': 'middle', class: 'rot' }).forEach(([k, v]) => tx.setAttribute(k, v));
  tx.style.fontSize = '64px'; tx.textContent = 'REFRESCA?';
  const risco = document.createElementNS(NS, 'line');
  Object.entries({ x1: 300, y1: 1230, x2: 640, y2: 1230, stroke: '#ff2d2d', 'stroke-width': 12, 'stroke-linecap': 'round' }).forEach(([k, v]) => risco.setAttribute(k, v));
  g.append(tx, risco); g.style.opacity = 0; return { g, risco };
})();

// ---------------------------------------------------------------- fecho: a cena encolhe para dentro de um celular
const CEL = { s: 0.56, cx: 540, cy: 880 };
function fecho(t) {
  const a = B.b6.ini - 0.1;
  const k = io(ramp(t, a, a + 1.1));
  const s = lerp(1, CEL.s, k), w = 1080 * s, h = 1920 * s;
  const x = lerp(0, CEL.cx - (1080 * CEL.s) / 2, k), y = lerp(0, CEL.cy - (1920 * CEL.s) / 2, k);
  const tela = $('tela');
  tela.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
  tela.style.borderRadius = `${lerp(0, 50 / CEL.s, k)}px`;
  $('fundo').style.opacity = k;
  const cel = $('celular');
  cel.style.opacity = ramp(t, a + 0.5, a + 1.0);
  Object.assign(cel.style, { left: `${x - 14}px`, top: `${y - 14}px`, width: `${w + 28}px`, height: `${h + 28}px` });
  // o botão Enviar aparece dentro da tela, embaixo; o dedo toca nele
  const env = $('enviar');
  const bx = CEL.cx, by = CEL.cy + (1920 * CEL.s) / 2 - 150;
  const ap = out3(ramp(t, a + 1.0, a + 1.4));
  const aperto = Math.sin(Math.PI * ramp(t, T.toque, T.toque + 0.35));
  env.style.opacity = ap;
  env.style.left = `${bx - 120}px`; env.style.top = `${by - 44}px`;
  env.style.transform = `scale(${(0.9 + 0.1 * ap) * (1 - 0.08 * aperto)})`;
  env.style.background = aperto > 0.3 || t > T.toque + 0.35 ? '#ffe36b' : '#FACC15';
  const dedo = $('dedo');
  const chega = io(ramp(t, T.toque - 0.7, T.toque));
  dedo.style.opacity = Math.min(ramp(t, T.toque - 0.8, T.toque - 0.5), 1 - ramp(t, FIM - 0.6, FIM - 0.2));
  dedo.style.left = `${lerp(bx + 220, bx - 60, chega) }px`; dedo.style.top = `${lerp(by + 260, by - 60, chega)}px`;
  dedo.style.transform = `scale(${1 - 0.25 * aperto})`;
}

// ---------------------------------------------------------------- quadro a quadro
function renderAt(t) {
  fotos(t);
  camera(t);

  // ondas de calor (cor do calor, sempre a mesma)
  ondas(t, 'frente', Math.max(
    t < corte('b1') + 0.3 ? lerp(0.55, 1, out3(ramp(t, T.esquenta - 0.1, T.esquenta + 0.4))) * (1 - ramp(t, corte('b1'), corte('b1') + 0.3)) : 0, 0));
  ondas(t, 'aberta', win(t, T.esquenta1 - 0.1, corte('b2') + 0.2, 0.4, 0.3));
  ondas(t, 'tras', win(t, T.grade4 - 0.1, T.f6 + 0.3, 0.4, 0.3), 170);
  ondas(t, 'grade', win(t, T.f6, corte('b5') + 0.3, 0.4, 0.3) * lerp(0.6, 1, ramp(t, T.junto - 0.2, T.junto + 0.4)), 190);
  ondas(t, 'volta', win(t, T.cozinha7, T.f8 + 0.3, 0.5, 0.3), 170);
  ondas(t, 'fim', T.f8 <= t ? out3(ramp(t, T.aquecedor - 0.2, T.aquecedor + 0.4)) : 0, 160);

  // brilho da grade e da geladeira "aquecedor"
  $('br-tras').style.opacity = win(t, T.grade4 - 0.1, T.f6 + 0.3, 0.5, 0.3) * lerp(0.75, 1, ramp(t, T.tomada, T.tomada + 0.5));
  $('br-grade').style.opacity = win(t, T.f6, corte('b5') + 0.3, 0.4, 0.3) * lerp(0.55, 1, ramp(t, T.junto - 0.2, T.junto + 0.5));
  $('br-frente').style.opacity = t >= T.f8 ? out3(ramp(t, T.aquecedor - 0.2, T.aquecedor + 0.5)) * 0.9 : (t < corte('b1') ? 0.35 * out3(ramp(t, T.esquenta - 0.1, T.esquenta + 0.5)) : 0);

  // calor de dentro correndo para o fundo e saindo
  const vDentro = win(t, T.calor3 - 0.1, corte('b3') + 0.2, 0.35, 0.3);
  gDentro.style.opacity = vDentro;
  SETAS_DENTRO.forEach((p) => p.setAttribute('stroke-dashoffset', (-t * 140).toFixed(1)));
  gSobe.style.opacity = win(t, palavra('f3', 'fora') - 0.2, corte('b3') + 0.2, 0.35, 0.3);
  SETA_SOBE.setAttribute('stroke-dashoffset', (-t * 160).toFixed(1));

  // o frio escorre pela porta (azul-claro só para ele)
  gFrio.style.opacity = Math.max(win(t, F.f1.ini - 0.1, corte('b2') + 0.3, 0.4, 0.4) * 0.95, win(t, corte('b5') + 0.1, T.f8 + 0.3, 0.4, 0.3));
  SETAS_FRIO.forEach((p) => p.setAttribute('stroke-dashoffset', (-t * 120).toFixed(1)));

  // energia da tomada até o motor
  gLuz.style.opacity = win(t, T.tomada - 0.15, T.f6 + 0.2, 0.3, 0.3);
  SETA_LUZ.setAttribute('stroke-dashoffset', (-t * 220).toFixed(1));

  // rótulos
  R_CONDENSADOR.style.opacity = win(t, T.grade4 + 0.1, corte('b4') + 0.2, 0.35, 0.3);
  R_MOTOR.style.opacity = win(t, T.motor - 0.05, T.f6 + 0.2, 0.35, 0.3);
  R_REFRESCA.g.style.opacity = win(t, F.f1.ini + 0.2, corte('b2') + 0.1, 0.35, 0.3);
  const risca = out3(ramp(t, T.esquenta1 - 0.05, T.esquenta1 + 0.3));
  R_REFRESCA.risco.setAttribute('x2', lerp(300, 640, risca));
  R_REFRESCA.risco.style.opacity = risca > 0 ? 1 : 0;

  // gancho escrito no quadro 0, depois a legenda assume (em cima)
  const fimG = F.g.fim + 0.3;
  $('gancho').style.opacity = 1 - ramp(t, fimG - 0.25, fimG);
  legenda(t < fimG ? -1 : t);
  cartoes(t);
  fecho(t);
}

// ---------------------------------------------------------------- ligação com o HyperFrames (espera fontes e fotos)
window.addEventListener('hf-seek', (e) => renderAt(e.detail.time));
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
const fontes = ['800 40px Sora', '700 40px Inter', '700 40px "JetBrains Mono"'].map((f) => document.fonts.load(f));
const imgs = [...document.querySelectorAll('img.foto')].map((i) => i.decode().catch(() => {}));
window.__hf.buildReady['geladeira'] = Promise.all([...fontes, ...imgs]).catch(() => {}).then(() => renderAt(window.__hfThreeTime || 0));
renderAt(window.__hfThreeTime || 0);
