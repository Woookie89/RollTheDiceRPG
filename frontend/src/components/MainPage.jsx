import { useState } from 'react';

const dice = [4, 6, 8, 10, 12, 20];

function QuickRoll() {
    const [die, setDie] = useState(20);
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [rollId, setRollId] = useState(0);

    const roll = () => {
        const nextResult = Math.floor(Math.random() * die) + 1;

        setResult(nextResult);
        setHistory(current => [
            { die, result: nextResult, id: rollId + 1 },
            ...current,
        ].slice(0, 4));
        setRollId(current => current + 1);
    };

    return (
        <div className="roll-console" aria-label="Rzut próbny">
            <div className="die-selector" aria-label="Wybierz rodzaj kości">
                {dice.map(sides => (
                    <button
                        key={sides}
                        type="button"
                        className="die-button"
                        aria-pressed={die === sides}
                        onClick={() => setDie(sides)}
                    >
                        D{sides}
                    </button>
                ))}
            </div>

            <div className="roll-stage">
                <div className="roll-result" aria-live="polite">
                    <span>Wynik D{die}</span>
                    <strong key={rollId}>{result ?? '?'}</strong>
                </div>
                <button type="button" className="roll-button" onClick={roll}>
                    Rzuć kością
                </button>
            </div>

            <div className="roll-history">
                <span>Ostatnie rzuty</span>
                {history.length > 0 ? (
                    <ol>
                        {history.map(item => (
                            <li key={item.id}>
                                <span>D{item.die}</span>
                                <strong>{item.result}</strong>
                            </li>
                        ))}
                    </ol>
                ) : (
                    <p>Wybierz kość i wykonaj pierwszy rzut.</p>
                )}
            </div>
        </div>
    );
}

function MainPage() {
    return (
        <main>
            <section className="hero-section">
                <div className="hero-copy">
                    <p className="hero-eyebrow">Twój stół, jedna przeglądarka</p>
                    <h1>Każda sesja ma swoje miejsce.</h1>
                    <p className="hero-lead">
                        Prowadź kampanię, karty postaci, rzuty i dziennik bez
                        przełączania się między narzędziami.
                    </p>
                    <div className="hero-actions">
                        <a href="/login" className="button button-primary">
                            Wejdź do gry
                        </a>
                        <a href="/register" className="button button-secondary">
                            Załóż konto
                        </a>
                    </div>
                </div>

                <figure className="hero-visual">
                    <img
                        src="/images/rpg-table-hero.png"
                        alt="Stół do sesji RPG z mapą, dziennikiem i zestawem kości"
                        width="1536"
                        height="864"
                        fetchPriority="high"
                    />
                </figure>
            </section>

            <section className="quick-roll-section" id="quick-roll">
                <div className="section-copy">
                    <h2>Rzut próbny, bez karty postaci.</h2>
                    <p>
                        Wybierz kość i sprawdź mechanikę stołu. Wyniki zostają
                        pod ręką, dokładnie jak podczas sesji.
                    </p>
                </div>
                <QuickRoll />
            </section>

            <section className="workspace-section">
                <div className="workspace-heading">
                    <h2>Od pierwszego rzutu do końca kampanii.</h2>
                    <p>
                        Jedno miejsce na najważniejsze elementy wspólnej gry.
                    </p>
                </div>

                <div className="workspace-features">
                    <article>
                        <span>01</span>
                        <h3>Karta postaci</h3>
                        <p>Atrybuty, zasoby i notatki zawsze przy stole.</p>
                    </article>
                    <article>
                        <span>02</span>
                        <h3>Historia rzutów</h3>
                        <p>Każdy wynik zapisany w kontekście sesji.</p>
                    </article>
                    <article>
                        <span>03</span>
                        <h3>Dziennik drużyny</h3>
                        <p>Decyzje i tropy, do których łatwo wrócić.</p>
                    </article>
                    <article>
                        <span>04</span>
                        <h3>Wiele systemów</h3>
                        <p>Wspólny stół przygotowany na różne zasady.</p>
                    </article>
                </div>
            </section>
        </main>
    );
}

export default MainPage;
