//
//  PhotoDetailView.swift
//  mobile
//

import SwiftUI

struct TagSelectionView: View {
    @Binding var taglist: [PhotoTag]
    @Binding var selectedtags: [Bool]
    var body: some View {
        List {
            ForEach(0..<taglist.count) { idx in
                Toggle(isOn: $selectedtags[idx]) {
                    Text(taglist[idx].Name)
                }
            }
        }
    }
}

struct PhotoDetailView: View {
    @Binding var image: UIImage?
    @Binding var photo: MetaPhoto?
    @Binding var new: Bool
    @State var allTags: [PhotoTag]
    @Binding var selectedTags: [Bool]
    var onSave: () -> Void
    
    var body: some View {
        NavigationStack {
            VStack {
                if let img = image {
                    Image(uiImage: img)
                        .resizable()
                        .scaledToFit()
                }
                List {
                    if let unwrappedMeta = photo {
                        TextField("Название", text: Binding(
                            get: { unwrappedMeta.Name },
                            set: { photo?.Name = $0 }
                        ))
                        
                        TextField("Описание", text: Binding(
                            get: { unwrappedMeta.Description },
                            set: { photo?.Description = $0 }
                        ))
                        
                        NavigationLink {
                            TagSelectionView(
                                taglist: $allTags,
                                selectedtags: $selectedTags
                            )
                        } label: {
                            Text("Выберите теги")
                        }
                    }
                }
                HStack {
                    Spacer()
                    Button (action: {
                        photo?.Tags = []
                        for idx in 1..<allTags.count {
                            if selectedTags[idx] {
                                photo?.Tags.append(allTags[idx])
                            }
                        }
                        onSave()
                    }) {
                        Text("Сохранить")
                    }
                    .buttonStyle(.borderedProminent)
                    Spacer()
                }
            }
        }
    }
}

/*
struct PhotoDetailView_Previews: PreviewProvider {
    static var previews: some View {
        PhotoDetailView()
    }
}
*/
