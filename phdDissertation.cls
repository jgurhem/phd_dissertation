% =========================================================================
% Latex Style for PhD dissertations at University of Lille
%
% author ; Jérôme Gurhem

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{phdDissertation}

\LoadClass[twoside,11pt,a4paper]{book}

\RequirePackage[utf8]{inputenc}
\RequirePackage[french, english]{babel}
\frenchspacing
\RequirePackage[T1]{fontenc}
\RequirePackage[top=30mm,bottom=30mm,left=15mm,right=15mm]{geometry}
\RequirePackage{graphicx}

\renewcommand{\baselinestretch}{1.213}


% =============================================
% Page de garde
% =============================================

\def\titleFR#1{\gdef\@titleFR{#1}}
\def\titleEN#1{\gdef\@titleEN{#1}}
\def\abstractFR#1{\gdef\@abstractFR{#1}}
\def\abstractEN#1{\gdef\@abstractEN{#1}}
\def\keywordsFR#1{\gdef\@keywordsFR{#1}}
\def\keywordsEN#1{\gdef\@keywordsEN{#1}}
\def\@author{}
\def\address#1{\gdef\@address{#1}}
\def\doctoralschool#1{\gdef\@doctoralschool{#1}}
\def\labo#1{\gdef\@labo{#1}}
\def\specialiteFR#1{\gdef\@specialiteFR{#1}}
\def\specialiteEN#1{\gdef\@specialiteEN{#1}}
\def\datesoumission#1{\gdef\@datesoumission{#1}}
\def\datesoutenanceFR#1{\gdef\@datesoutenanceFR{#1}}
\def\datesoutenanceEN#1{\gdef\@datesoutenanceEN{#1}}
\def\locationsoutenance#1{\gdef\@locationsoutenance{#1}}
\def\juryFR#1{\gdef\@juryFR{#1}}
\def\juryEN#1{\gdef\@juryEN{#1}}
\def\dirname#1{\gdef\@dirname{#1}}
\def\diraffiliationFR#1{\gdef\@diraffiliationFR{#1}}
\def\diraffiliationEN#1{\gdef\@diraffiliationEN{#1}}

\newcommand*{\universitylogo}[1]{\gdef\@universitylogo{#1}}
\universitylogo{}

\newcommand*{\universitylogoscale}[1]{\gdef\@universitylogoscale{#1}}
\universitylogoscale{}

\renewcommand{\titlepage}{%
	\includegraphics[scale=\@universitylogoscale]{\@universitylogo}
	\begin{center}
	\uppercase{\Large \textbf{Université de Lille}}

	\vspace{4mm}
	\@doctoralschool

	\@labo

	\vspace{12mm}
	\textsc{\huge \textbf{TH\`ESE}}

	\vspace{3mm}
	{\Large{préparée et soutenue publiquement}}

	\vspace{3mm}
	\textsc{\Large{par}}

	\vspace{3mm}
	\Large \textbf{{\@author}}

	\vspace{3mm}
	\large \textbf{à} {\@locationsoutenance}

	\vspace{3mm}
	\large \textbf{le} {\@datesoutenanceFR}

	\vspace{3mm}
	{\large pour obtenir le grade de Docteur en \textsc{\textbf{\@specialiteFR}}}
	\vspace{4mm}

	\noindent\rule{\linewidth}{0.5mm}
	{\setlength{\baselineskip}{1.2\baselineskip}
		\begin{huge}
		\textbf{\Large \@titleFR}

		\end{huge}
		\par}
	\vspace{0.2cm}
	\noindent\rule{\linewidth}{0.5mm}
	\bigskip
	\begin{flushleft}
	\textbf{Thèse dirigée par} \textsc{\@dirname}, \@diraffiliationFR
	\end{flushleft}

	\textsc{Membres du jury:}
	\vspace{0.5cm}

	{\small \@juryFR}

	\end{center}
	\cleardoublepage


	\includegraphics[scale=\@universitylogoscale]{\@universitylogo}
	\begin{center}
	\uppercase{\Large \textbf{University of Lille}}

	\vspace{4mm}
	\@doctoralschool

	\@labo

	\vspace{12mm}
	\textsc{\huge \textbf{Ph.D. Thesis}}

	\vspace{3mm}
	{\Large{prepared and defended}}

	\vspace{3mm}
	\textsc{\Large{by}}

	\vspace{3mm}
	\Large \textbf{{\@author}}

	\vspace{3mm}
	\large \textbf{à} {\@locationsoutenance}

	\vspace{3mm}
	\large \textbf{le} {\@datesoutenanceEN}

	\vspace{3mm}
	{\large to obtain the grade of Ph.D. in \textsc{\textbf{\@specialiteEN}}}
	\vspace{4mm}

	\noindent\rule{\linewidth}{0.5mm}
	{\setlength{\baselineskip}{1.2\baselineskip}
		\begin{huge}
		\textbf{\Large \@titleEN}

		\end{huge}
		\par}
	\vspace{0.2cm}
	\noindent\rule{\linewidth}{0.5mm}
	\bigskip
	\begin{flushleft}
	\textbf{Thesis advised by} \textsc{\@dirname}, \@diraffiliationEN
	\end{flushleft}

	\textsc{Committee members:}
	\vspace{0.5cm}

	{\small \@juryEN}

	\end{center}
	\cleardoublepage
}