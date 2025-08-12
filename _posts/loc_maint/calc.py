import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.patches as mpatches
import os

@dataclass
class Language:
    """Represents a programming language with its characteristics"""
    name: str
    dev_speed: float  # LOC per developer per workday
    feature_density: float  # Features per 1000 LOC (expressiveness)
    maintenance_burden: float  # Hours per 1000 LOC per sprint (2 weeks, includes tech debt effects)

# Define characteristics for various languages based on realistic metrics
languages = {
    'Python': Language('Python', 350, 5.0, 10.0),  # High expressiveness, moderate maintenance
    'Java': Language('Java', 400, 4.0, 3.0),      # Enterprise verbose, higher maintenance
    'C++': Language('C++', 200, 3.5, 5.0),        # Low level, high maintenance burden
    'Go': Language('Go', 500, 6.0, 1.0),          # Simple, designed for maintainability
    'JavaScript': Language('JavaScript', 350, 4.0, 3.8),  # Fast to write, messy to maintain
    'TypeScript': Language('TypeScript', 350, 5.0, 2.0),  # Better than JS, type safety helps
    'Rust': Language('Rust', 250, 3.0, 1.0),      # Slower to write, very maintainable
}

class SoftwareGrowthPDE:
    """
    Models software growth as a simplified system of coupled ODEs:
    - LOC: L(t) - total lines of code in thousands
    - Maintenance Hours: M(t) - hours per sprint required for maintenance
    
    Units:
    - Time: sprints (2-week periods)
    - LOC: thousands of lines of code (KLOC)
    - Work: hours per sprint (typically 80 hours/dev/sprint)
    """
    
    def __init__(self, language: Language, team_size: int):
        self.language = language
        self.team_size = team_size
        self.hours_per_dev_per_sprint = 80  # 2 weeks * 40 hours/week
        
    def system_equations(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        Simplified system of ODEs with critically damped behavior
        
        State vector y = [L, M] where:
        - L: Lines of code in KLOC (thousands)
        - M: Maintenance hours per sprint
        
        Args:
            t: Time in sprints
            y: State vector [L, M]
        
        Returns:
            Derivatives [dL/dt, dM/dt]
        """
        L, M = y
        
        # Total team capacity in hours per sprint
        total_hours = self.team_size * self.hours_per_dev_per_sprint
        
        # Hours available for new development (after maintenance)
        development_hours = max(0, total_hours - M)
        
        # Convert dev hours to LOC per sprint
        days_per_sprint = 10  # 2 weeks
        dL_dt = (development_hours / self.hours_per_dev_per_sprint) * self.language.dev_speed * days_per_sprint / 1000
        
        # Apply complexity slowdown as codebase grows (prevents overshoot)
        complexity_factor = 1.0 / (1.0 + 0.05 * L)  # Gentler slowdown
        dL_dt *= complexity_factor
        
        # Maintenance burden calculation (hours per sprint)
        # Required maintenance scales with codebase size
        required_maintenance = L * self.language.maintenance_burden
        
        # Cap required maintenance at total team capacity to prevent overshoot
        required_maintenance = min(required_maintenance, total_hours)
        
        # Critically damped adjustment to required maintenance level
        # Use lower adjustment rate to prevent overshoot
        adjustment_rate = 0.1  # Even slower, more stable adjustment
        dM_dt = (required_maintenance - M) * adjustment_rate
        
        # Ensure maintenance never exceeds total capacity
        if M + dM_dt * 0.01 > total_hours:  # Check against step size
            dM_dt = max(0, (total_hours - M) * adjustment_rate)
        
        return np.array([dL_dt, dM_dt])
    
    def solve(self, t_span: Tuple[float, float], t_eval: np.ndarray, 
              initial_loc: float = 2.0) -> dict:
        """
        Solve the system of ODEs
        
        Args:
            t_span: Time span (start, end)
            t_eval: Time points to evaluate
            initial_loc: Starting codebase size in KLOC
            
        Returns:
            Dictionary with solution arrays
        """
        # Initial conditions: [LOC in KLOC, Maintenance Hours]
        y0 = [initial_loc, initial_loc * self.language.maintenance_burden]
        
        # Solve with very tight tolerances and much smaller max step to prevent overshoot
        sol = solve_ivp(self.system_equations, t_span, y0, t_eval=t_eval, 
                       method='RK45', rtol=1e-10, atol=1e-12, max_step=0.01)
        
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        
        # Calculate derived metrics
        total_hours = self.team_size * self.hours_per_dev_per_sprint
        features = sol.y[0] * self.language.feature_density  # Features from LOC
        
        return {
            'time': sol.t,
            'loc': sol.y[0],  # KLOC
            'maintenance_hours': sol.y[1],  # Hours per sprint
            'features': features,  # Total features
            'loc_velocity': np.gradient(sol.y[0], sol.t),  # KLOC per sprint
            'feature_velocity': np.gradient(features, sol.t),  # Features per sprint
            'maintenance_fraction': sol.y[1] / total_hours,  # Fraction of team on maintenance
            'development_hours': np.maximum(0, total_hours - sol.y[1]),  # Hours for new dev
            'effective_devs': np.maximum(0, total_hours - sol.y[1]) / self.hours_per_dev_per_sprint
        }
    
    def analyze_equilibrium(self, solution: dict) -> dict:
        """Analyze when the system reaches equilibrium (LOC velocity ~ 0)"""
        loc_velocity = solution['loc_velocity']
        maintenance_fraction = solution['maintenance_fraction']
        time = solution['time']
        
        # Find when LOC velocity drops below threshold
        threshold = 0.05  # 50 LOC per sprint
        equilibrium_idx = np.where(loc_velocity < threshold)[0]
        
        # Find time to 50% maintenance
        half_maintenance_idx = np.where(maintenance_fraction >= 0.5)[0]
        if len(half_maintenance_idx) > 0:
            time_to_half_maintenance = time[half_maintenance_idx[0]]
        else:
            time_to_half_maintenance = None
        
        if len(equilibrium_idx) > 0:
            eq_time = time[equilibrium_idx[0]]
            eq_loc = solution['loc'][equilibrium_idx[0]]
            eq_features = solution['features'][equilibrium_idx[0]]
            eq_maintenance = solution['maintenance_fraction'][equilibrium_idx[0]]
        else:
            eq_time = time[-1]
            eq_loc = solution['loc'][-1]
            eq_features = solution['features'][-1]
            eq_maintenance = solution['maintenance_fraction'][-1]
            
        return {
            'equilibrium_time': eq_time,
            'max_loc': eq_loc,
            'max_features': eq_features,
            'maintenance_fraction_at_equilibrium': eq_maintenance,
            'time_to_half_maintenance': time_to_half_maintenance
        }

def create_individual_plots(languages_to_plot: List[str], team_size: int = 10):
    """Create individual plot files for each aspect of the system dynamics"""
    
    time_span = (0, 100)
    time_eval = np.linspace(0, 100, 1000)
    colors = plt.cm.tab10(np.linspace(0, 1, len(languages_to_plot)))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Store results for analysis
    results = {}
    for i, lang_name in enumerate(languages_to_plot):
        lang = languages[lang_name]
        model = SoftwareGrowthPDE(lang, team_size)
        solution = model.solve(time_span, time_eval)
        results[lang_name] = solution
    
    # Plot 1: LOC Growth
    plt.figure(figsize=(10, 6))
    for i, lang_name in enumerate(languages_to_plot):
        solution = results[lang_name]
        plt.plot(solution['time'], solution['loc'], 
                label=lang_name, color=colors[i], linewidth=2)
    
    plt.xlabel('Time (sprints)')
    plt.ylabel('Lines of Code (KLOC)')
    plt.title('Codebase Growth Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'codebase_growth.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: LOC Velocity (Log Scale)
    plt.figure(figsize=(10, 6))
    for i, lang_name in enumerate(languages_to_plot):
        solution = results[lang_name]
        # Only plot positive velocities for log scale
        positive_velocity = np.maximum(solution['loc_velocity'], 1e-6)  # Avoid log(0)
        plt.plot(solution['time'], positive_velocity, 
                label=lang_name, color=colors[i], linewidth=2)
    
    plt.xlabel('Time (sprints)')
    plt.ylabel('KLOC/Sprint (log scale)')
    plt.title('Development Velocity (Why Projects Slow Down)')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'development_velocity.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 3: Maintenance Hours
    plt.figure(figsize=(10, 6))
    for i, lang_name in enumerate(languages_to_plot):
        solution = results[lang_name]
        plt.plot(solution['time'], solution['maintenance_hours'], 
                label=lang_name, color=colors[i], linewidth=2)
    
    plt.xlabel('Time (sprints)')
    plt.ylabel('Maintenance Hours/Sprint')
    plt.title('Maintenance Burden Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'maintenance_burden.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 4: Team Allocation with 50% annotations
    plt.figure(figsize=(12, 8))
    half_maintenance_times = []
    
    for i, lang_name in enumerate(languages_to_plot):
        solution = results[lang_name]
        maintenance_pct = solution['maintenance_fraction'] * 100
        plt.plot(solution['time'], maintenance_pct, 
                label=f'{lang_name} (Maintenance)', color=colors[i], linewidth=2)
        plt.plot(solution['time'], 100 - maintenance_pct, 
                label=f'{lang_name} (Development)', color=colors[i], linewidth=2, linestyle='--')
        
        # Find time to 50% maintenance
        half_maintenance_idx = np.where(maintenance_pct >= 50.0)[0]
        if len(half_maintenance_idx) > 0:
            half_time = solution['time'][half_maintenance_idx[0]]
            half_maintenance_times.append((half_time, lang_name, colors[i]))
            
            # Add vertical line at 50% maintenance time
            plt.axvline(x=half_time, color=colors[i], linestyle='-', alpha=0.6, linewidth=1.5)
        else:
            half_maintenance_times.append((None, lang_name, colors[i]))
    
    # Add horizontal line at 50%
    plt.axhline(y=50, color='red', linestyle=':', alpha=0.7, linewidth=2, label='50% Threshold')
    
    # Add annotations at the bottom for time to 50% maintenance with staggered heights
    base_y = 2  # Base position near bottom of plot
    y_offsets = [0, 8, 16, 24, 32]  # Stagger heights to prevent overlap
    
    # Sort by half_time for better visual arrangement
    sorted_times = [(half_time, lang_name, color, i) for i, (half_time, lang_name, color) in enumerate(half_maintenance_times)]
    sorted_times.sort(key=lambda x: x[0] if x[0] is not None else float('inf'))
    
    for j, (half_time, lang_name, color, orig_idx) in enumerate(sorted_times):
        y_position = base_y + y_offsets[j % len(y_offsets)]
        
        if half_time is not None:
            plt.annotate(f'{lang_name}: {half_time:.0f}', 
                        xy=(half_time, y_position), 
                        ha='center', va='bottom',
                        fontsize=10, color=color, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor=color))
        else:
            # Place "never reached" annotation at the right side with staggered height
            plt.annotate(f'{lang_name}: Never', 
                        xy=(85, y_position), 
                        ha='center', va='bottom',
                        fontsize=10, color=color, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor=color))
    
    plt.xlabel('Time (sprints)')
    plt.ylabel('Team Allocation (%)')
    plt.title('Development vs Maintenance Allocation\n(Vertical lines show time to 50% maintenance)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 105)  # Give some room at top
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'team_allocation.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 5: Feature Accumulation
    plt.figure(figsize=(10, 6))
    for i, lang_name in enumerate(languages_to_plot):
        solution = results[lang_name]
        plt.plot(solution['time'], solution['features'], 
                label=lang_name, color=colors[i], linewidth=2)
    
    plt.xlabel('Time (sprints)')
    plt.ylabel('Total Features')
    plt.title('Feature Accumulation Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'feature_accumulation.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    return results

def analyze_carrying_capacity(languages_to_plot: List[str], team_size: int = 10):
    """Analyze equilibrium points and carrying capacity"""
    
    time_span = (0, 200)  # Longer time to reach equilibrium
    time_eval = np.linspace(0, 200, 2000)
    
    print(f"\nCarrying Capacity Analysis (Team Size: {team_size})")
    print("=" * 80)
    
    for lang_name in languages_to_plot:
        lang = languages[lang_name]
        model = SoftwareGrowthPDE(lang, team_size)
        solution = model.solve(time_span, time_eval)
        analysis = model.analyze_equilibrium(solution)
        
        print(f"\n{lang_name}:")
        print(f"  Max Codebase Size: {analysis['max_loc']:.1f} KLOC")
        print(f"  Max Features: {analysis['max_features']:.0f}")
        print(f"  Time to 50% Maintenance: {analysis['time_to_half_maintenance']:.1f} sprints" if analysis['time_to_half_maintenance'] else "  Time to 50% Maintenance: Never reached")
        print(f"  Time to Equilibrium: {analysis['equilibrium_time']:.1f} sprints")
        print(f"  Maintenance % at Equilibrium: {analysis['maintenance_fraction_at_equilibrium']*100:.1f}%")
        print(f"  Language Characteristics:")
        print(f"    Dev Speed: {lang.dev_speed:.0f} LOC/dev/day")
        print(f"    Feature Density: {lang.feature_density:.1f} features/KLOC")
        print(f"    Maintenance Burden: {lang.maintenance_burden:.1f} hours/KLOC/sprint")

def team_size_analysis(lang_name: str, team_sizes: List[int]):
    """Analyze impact of team size (Brooks's Law effect)"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{lang_name}: Team Size Impact Analysis', fontsize=16)
    
    time_span = (0, 150)
    time_eval = np.linspace(0, 150, 1500)
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(team_sizes)))
    
    lang = languages[lang_name]
    
    # Plot 1: LOC growth
    ax1 = axes[0, 0]
    for i, team_size in enumerate(team_sizes):
        model = SoftwareGrowthPDE(lang, team_size)
        solution = model.solve(time_span, time_eval)
        ax1.plot(solution['time'], solution['loc'], 
                label=f'{team_size} devs', color=colors[i], linewidth=2)
    
    ax1.set_xlabel('Time (sprints)')
    ax1.set_ylabel('Codebase Size (KLOC)')
    ax1.set_title('Codebase Growth by Team Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: LOC velocity
    ax2 = axes[0, 1]
    for i, team_size in enumerate(team_sizes):
        model = SoftwareGrowthPDE(lang, team_size)
        solution = model.solve(time_span, time_eval)
        ax2.plot(solution['time'], solution['loc_velocity'], 
                label=f'{team_size} devs', color=colors[i], linewidth=2)
    
    ax2.set_xlabel('Time (sprints)')
    ax2.set_ylabel('KLOC/Sprint')
    ax2.set_title('Development Velocity by Team Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Carrying capacity vs team size
    ax3 = axes[1, 0]
    max_loc = []
    for team_size in team_sizes:
        model = SoftwareGrowthPDE(lang, team_size)
        solution = model.solve(time_span, time_eval)
        max_loc.append(solution['loc'][-1])
    
    ax3.plot(team_sizes, max_loc, 'bo-', linewidth=2, markersize=8)
    ax3.set_xlabel('Team Size')
    ax3.set_ylabel('Max Codebase Size (KLOC)')
    ax3.set_title('Carrying Capacity vs Team Size')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Efficiency (KLOC per developer)
    ax4 = axes[1, 1]
    efficiency = [loc/t for loc, t in zip(max_loc, team_sizes)]
    ax4.plot(team_sizes, efficiency, 'ro-', linewidth=2, markersize=8)
    ax4.set_xlabel('Team Size')
    ax4.set_ylabel('KLOC per Developer')
    ax4.set_title('Developer Efficiency (Brooks\'s Law)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save to same directory as script  
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(script_dir, 'team_size_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()

# Run demonstrations
if __name__ == "__main__":
    # Create individual plot files
    print("Running Software Development System Dynamics Analysis...")
    results = create_individual_plots(['Python', 'Java', 'C++', 'TypeScript', 'Rust'], team_size=10)
    
    # Carrying capacity analysis
    analyze_carrying_capacity(['Python', 'Java', 'C++', 'TypeScript', 'Rust'], team_size=10)
    
    # Team size analysis (Brooks's Law)
    print("\nAnalyzing team size effects (Brooks's Law)...")
    team_size_analysis('Python', [5, 10, 20, 40, 80])