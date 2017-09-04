% given a set of quality and similarity matrices, select the k best
% sentences from each document

n_selections = 10;

qual = load('qual.mat');
qual = orderfields(qual);
qual_fields = fieldnames(qual);

sim = load('sim.mat');
sim = orderfields(sim);
sim_fields = fieldnames(sim);

Selections = [];

%function Curr_Selections = calc_DPP(qual_mat,sim_mat)
for curr_doc = 1 : length(qual_fields)
    qual_mat = qual.(char(qual_fields(curr_doc)));
    sim_mat = sim.(char(sim_fields(curr_doc)));
    
    L = sim_mat .* (qual_mat*qual_mat');       
    L = 0.5*(L+L');
    [V, Lam] = eig(full(L));
    Lam(Lam<0) = 0;
    L = V*Lam*V';

    candidates = true(length(qual_mat),1);

    Curr_Selections = [];
    val_old = 0;

    for t = 1 : n_selections
        inds = find(candidates);
        p = zeros(size(inds));
        
        for iter = 1 : length(inds)
            i = inds(iter);
            Curr_Selections_tmp = [i; Curr_Selections];
            p(iter) = (det(L(Curr_Selections_tmp,Curr_Selections_tmp)) - val_old);
        end
        
        [val, pos] = max(p);
        Curr_Selections = [inds(pos); Curr_Selections];
        val_old = det(L(Curr_Selections,Curr_Selections));
        candidates(Curr_Selections) = false;
    end
    
    Selections = horzcat(Curr_Selections, Selections);
end

Selections = Selections';
save('sel.mat','Selections');