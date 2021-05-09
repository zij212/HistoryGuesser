<template>
  <div class="about container">
    <section class="section">
      <p class="title">The Game</p>
      <p class="subtitle">
        History Guesser is an educational game where you are matched with a random figure from history.

        The goal is to figure out who it is by talking to them.  Maybe it is Leonardo da Vinci.. or Genghis Kahn.

        You have a limited amount of questions you can ask, and will only get limited information back -- so choose wisely!
      </p>
    </section>
    <section class="section">

      <p class="title">How it works</p>
      <p class="subtitle">
        Since you can't actually speak to the real people, we are using OpenAI's davinci AI to act like random historical figures.
        Behind the scenes, The AI is instructed to be a random person.  And then a conversation can be had!
      </p>

      <div>
        <span class="has-text-weight-bold has-text-danger">Warning</span>: This is powered by AI.  Some answers will be off, but most will be accurate.
      </div>
      <div>
        We try our best to accept multple versions of names and places, and everything is case sensitive. Sorry for any typos/mistakes on our part!
      </div>
    </section>
  </div>
</template>
