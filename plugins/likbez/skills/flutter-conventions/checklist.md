# Flutter convention checklist

Two tiers: **must-read** = not enforced by analyzer/DCM — a reviewer/implementer must check by
reading; **dcm-caught** = enforced mechanically by the analyzer/DCM gate — listed only so nobody
re-reports them.

## must-read

Architecture & layering (`docs/conventions.md`, `CLAUDE.md` §Repository Pattern):
- [ ] Domain never uses API-client types — domain models get `fromApi` factories
      (`tryFromApi`/`tryFromDb` when nullable). Generated client types stay in `lib/data/`.
- [ ] Repository split: `abstract interface class` + `Impl` suffix; **Impl method signatures
      exactly match the interface** — same parameter names, types, and order.
- [ ] Interface methods carry doc comments.
- [ ] Widgets never construct domain services or touch repositories directly — use
      `DomainServiceFactory` in screen-level listeners (the `AuthenticationDialog` pattern) or
      dispatch BLoC events. Exception: `lib/feature/settings/debug/view/`.
- [ ] One model per file, placed in `lib/data/model/{domain}/` — never co-located in
      DAO/repository/BLoC files.
- [ ] Presentation → Domain → Data direction only; feature code stays inside its
      `lib/feature/<feature>/` module; scoped DI via the feature's `Scope` widget + `BlocFactory`
      (`context.someScopeBlocFactory.someBloc()`), never a service locator, never
      `BlocProvider.value`.
- [ ] No bare `Function`/closure constructor params through DI factories — inject
      repositories/services instead (e.g. `WindowRepository.isFocused()`).

Widget rules not lint-covered (`CLAUDE.md` §Widget Rules, `docs/code_style_guide.md` §Widgets):
- [ ] No private `_build*` methods returning a widget tree — inline in `build()`, extract a
      private widget class, or move to a separate file. (`prefer-widget-private-members` is a
      different DCM rule — it checks that State fields are private, not that build helpers don't
      exist.)
- [ ] No `part`/`part of` outside generated files — each widget in its own file (exception:
      freezed `part` directives for BLoC events/states/actions).
- [ ] Prefer `DecoratedBox` (+ `SizedBox`/`ConstrainedBox` for sizing) over `Container` when only
      decorating (background/border/shape/gradient) — `use_decorated_box` only catches the
      trivial no-size case, so a sized/constrained decorated box needs a manual check. Watch the
      border-inset gotcha (`BoxDecoration.border` insets a `Container`'s child like padding;
      `DecoratedBox` paints on the edge without resizing). `Container` is reserved for debug-only
      screens.

BLoC (`CLAUDE.md` §BLoC Patterns):
- [ ] Events named as past actions (`ThemeChanged`, `ButtonPressed`); single freezed state class
      with a status enum — not multiple factory constructors.
- [ ] All mutable state lives in the State class (exception: `StreamSubscription` fields).
- [ ] `ActionBloc` for one-time events (navigation, dialogs, snackbars).
- [ ] `isClosed` guard **only** when an `emit()`/`action()` follows an `await` — a guard anywhere
      else is dead code; its absence before a post-await emit is a bug.
- [ ] `late final StreamSubscription` (not `StreamSubscription?`) when always assigned and always
      cancelled in `close()`.

Logging & time (`docs/conventions.md` §Logging):
- [ ] No `[ClassName]` prefixes in log messages — the logger records the call site.
- [ ] `DateTimeRepository.now()` / `.timestamp()` — never `DateTime.now()` (DCM catches direct
      calls, but also watch for indirect wrappers reintroducing it).

Structure & style not lint-covered:
- [ ] Dependency versions sorted alphabetically (`CLAUDE.md` §Critical Conventions).
- [ ] No dead code / commented-out code; decompose methods over ~80 lines; numeric literals
      (except 0/1/-1) and repeated strings become named constants.
- [ ] Screen structure: `BlocProvider` → `ShimmerScope` → `Scaffold` → `CustomAppBar` → `SafeArea`;
      lifecycle observer = outer StatelessWidget + inner StatefulWidget with
      `WidgetsBindingObserver`.
- [ ] `RefreshButton` (desktop) / `CustomRefreshIndicator` (mobile) disabled during all loading
      states.
- [ ] No `!` (null assertion) operator — extract to a local variable, null-check, or let Dart
      promote the type. No analyzer/DCM rule bans this operator; it is review-enforced only.
- [ ] Prefer a `const` constructor when every instance field is `final` with no non-const
      initializers. `prefer_const_constructors` only flags call sites that could be const, never
      the declaration; `prefer_const_constructors_in_immutables` only covers `@immutable`-annotated
      classes — every other class needs a manual check.
- [ ] Avoid boolean flags for behavior modes (constructor/method params, not just BLoC state) —
      prefer an enum or separate methods.
- [ ] Avoid repeated subscript/collection access — extract `map[key]` (or similar) to a local
      variable when read more than once instead of re-indexing.
- [ ] No hand-edits to generated files (`*.g.dart`, `*.freezed.dart`, generated asset/l10n
      trees — the `analysis_options.yaml` exclude list): the fix belongs in the source (annotated
      model, ARB file, SVG, API spec) followed by your project's codegen command. Codegen emits
      new symbols into the generated `part` files, so any code-search index the repo keeps (an
      `ast-index` database, say) stays blind to them until it is refreshed.

Sensitive surfaces (always high-severity findings):
- [ ] Security-sensitive code paths — key material, credential storage, lockers, DB encryption
      and its migrations — demand explicit justification in the PR/plan for any touch;
      identity/account derivation goes through the designated single source, never ad-hoc.

## dcm-caught (informational — the analyzer/DCM gate enforces these)

- No Cubits (`avoid-cubits`); no public BLoC fields/methods; every event subclass handled.
- Member ordering (static const → final → constructors → late → initialized → nullable → getters →
  init → overrides → public → dispose/close → private; widget variant differs).
- No `print`; `DateTime.now()` ban; `flutter_style_todos`; single quotes; always curly braces;
  120-col line length + `trailing_commas: preserve`.
- File name matches class name (`prefer-match-file-name`); no initialized fields in
  StatelessWidget; parameter ordering (`super` → `required` → default-last).
- Pinned dependency versions, no caret (`prefer-pinned-version-syntax` via `pubspec-rules`).
