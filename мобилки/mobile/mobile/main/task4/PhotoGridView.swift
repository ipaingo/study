//
//  PhotoGridView.swift
//  mobile
//

import SwiftUI

struct TagSelectionView_test: View {
    @Binding var taglist: [PhotoTag]
    @Binding var selectedtags: [Bool]
    var body: some View {
        List {
            ForEach(1..<taglist.count) { idx in
                Toggle(isOn: $selectedtags[idx]) {
                    Text(taglist[idx].Name)
                }
            }
        }
    }
}

struct PhotoGridView: View {
    @State private var TagList: [PhotoTag] = [
        PhotoTag(id: 0, Name: "Дом"),
        PhotoTag(id: 1, Name: "Работа"),
        PhotoTag(id: 2, Name: "Питомцы"),
        PhotoTag(id: 3, Name: "Развлечения")
    ]
    
    @State private var selected: Int = 0
    @State private var name: String = ""
    @State private var tags: [Bool] = [false, false, false, false]
    
    var body: some View {
        NavigationStack {
            List {
                VStack {
                    VStack {
                        //
                    }
                    .frame(width: 200.0, height: 200.0)
                    .background(Color(red: 0.9, green: 0.9, blue: 0.9))
                    
                    Text("Выбранные теги:")
                    
                    List {
                        ForEach(1..<TagList.count) { idx in
                            Text("\(TagList[idx].Name): \(tags[idx] ? "yes" : "no")")
                        }
                    }
                    
                    // NavigationStack {
                    NavigationLink {
                        TagSelectionView_test(
                           taglist: $TagList,
                           selectedtags: $tags
                        )
                    } label: {
                        Text("Выберите теги")
                    }
                    
                    Button {
                        //
                    } label: {
                        Text("Жмяк")
                    }
                    .buttonStyle(.borderless)
                    .padding()
                }
            }
        }
    }
}

struct PhotoGridView_Previews: PreviewProvider {
    static var previews: some View {
        PhotoGridView()
    }
}
